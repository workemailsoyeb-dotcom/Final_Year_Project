import os
import subprocess
import threading
import uuid
from flask import Flask, request, render_template, redirect, url_for, send_from_directory

import webapp_helpers as helpers

app = Flask(__name__)

_ACTIVE_REQUESTS = {}
_ACTIVE_REQUESTS_LOCK = threading.Lock()


def _curve_coeffs_from_form(form_data):
    return [
        form_data.get('Coeff_a1', '0'),
        form_data.get('Coeff_a2', '0'),
        form_data.get('Coeff_a3', '0'),
        form_data.get('Coeff_a4', '0'),
        form_data.get('Coeff_a6', '0'),
    ]


def _build_point_command(script_name, form_data, include_second_point=False, include_scalar=False):
    base_field = form_data['Base_Field']
    degree = form_data['Degree']
    choice = form_data.get('Choice_of_Coeff', '0')
    coeffs = _curve_coeffs_from_form(form_data)

    if choice == '1':
        # Point scripts already handle random coefficients/points internally for choice=1.
        return ['sage', f'scripts/{script_name}', base_field, degree, '1']

    cmd = ['sage', f'scripts/{script_name}', base_field, degree, choice]
    cmd.extend(coeffs)

    if include_second_point:
        cmd.extend([
            form_data.get('Point1_x', '0'),
            form_data.get('Point1_y', '0'),
            form_data.get('Point2_x', '0'),
            form_data.get('Point2_y', '0'),
        ])

    if include_scalar:
        cmd.extend([
            form_data.get('Point1_x', '0'),
            form_data.get('Point1_y', '0'),
            form_data.get('Scalar', '0'),
        ])

    return cmd


def _request_scope(scope_name):
    client_id = request.headers.get('X-Client-Id', '').strip() or (request.remote_addr or 'anonymous')
    return f"{client_id}:{scope_name}"


def _run_managed_command(cmd, scope_name, timeout=120):
    process_id = str(uuid.uuid4())
    request_key = _request_scope(scope_name)

    with _ACTIVE_REQUESTS_LOCK:
        previous = _ACTIVE_REQUESTS.get(request_key)
        if previous and previous['process'].poll() is None:
            previous['process'].terminate()

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        _ACTIVE_REQUESTS[request_key] = {'id': process_id, 'process': process}

    try:
        stdout, stderr = process.communicate(timeout=timeout)
        return stdout, stderr
    except subprocess.TimeoutExpired:
        process.kill()
        process.communicate()
        raise
    finally:
        with _ACTIVE_REQUESTS_LOCK:
            current = _ACTIVE_REQUESTS.get(request_key)
            if current and current['id'] == process_id:
                _ACTIVE_REQUESTS.pop(request_key, None)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/credits')
def credits():
    return render_template('credits.html')


@app.route('/calculate')
def calculate():
    return redirect(url_for('home'))


@app.route('/point_add')
def point_add():
    return redirect(url_for('home'))


@app.route('/point_multiply')
def point_multiply():
    return redirect(url_for('home'))


@app.route('/point_divide')
def point_divide():
    return redirect(url_for('home'))


@app.route('/point_substract')
def point_substract():
    return redirect(url_for('home'))


@app.route('/styles/<path:filename>')
def template_styles(filename):
    return send_from_directory(helpers.get_template_styles_dir(), filename)


@app.route('/calculate', methods=['POST'])
def run_script():
    try:
        form_data = request.form.to_dict()
        base_field = form_data['Base_Field']
        degree = form_data['Degree']
        choice = form_data['Choice_of_Coeff']
        plot_points = form_data.get('Plot_Points', '1')
        plot_curve = form_data.get('Plot_Curve', '1')

        coeffs = [
            form_data.get('Coeff_a1', '0'),
            form_data.get('Coeff_a2', '0'),
            form_data.get('Coeff_a3', '0'),
            form_data.get('Coeff_a4', '0'),
            form_data.get('Coeff_a6', '0'),
        ]

        if choice == '1':
            coeffs = helpers.generate_random_nonsingular_coeffs(base_field, degree)
            cmd = ['sage', 'scripts/find_Curve_Order.py', base_field, degree, '0']
            cmd.extend(coeffs)
            choice_for_plot = '0'
        else:
            cmd = ['sage', 'scripts/find_Curve_Order.py', base_field, degree, choice]
            cmd.extend(coeffs)
            choice_for_plot = choice

        output, error = _run_managed_command(cmd, '/calculate', timeout=120)

        points_plot = ""
        points_plot_error = ""
        if plot_points == '1':
            try:
                points_plot = helpers.generate_plot_image_base64(
                    base_field,
                    degree,
                    choice_for_plot,
                    coeffs,
                    plot_type='points',
                )
            except Exception as plot_exc:
                points_plot_error = str(plot_exc)

        curve_plot = ""
        curve_plot_error = ""
        if plot_curve == '1':
            try:
                curve_plot = helpers.generate_plot_image_base64(
                    base_field,
                    degree,
                    choice_for_plot,
                    coeffs,
                    plot_type='curve',
                )
            except Exception as plot_exc:
                curve_plot_error = str(plot_exc)

        return helpers.result_fragment(
            output=output,
            error=error,
            plot_points=points_plot,
            plot_points_error=points_plot_error,
            plot_curve=curve_plot,
            plot_curve_error=curve_plot_error,
        )

    except subprocess.TimeoutExpired:
        return helpers.result_fragment(error="Calculation timed out after 120 seconds.")
    except Exception as e:
        return helpers.result_fragment(error=str(e))


@app.route('/list_points')
def list_points():
    return redirect(url_for('home'))


@app.route('/list_points', methods=['POST'])
def run_list_points():
    try:
        form_data = request.form.to_dict()
        base_field = form_data['Base_Field']
        degree = form_data['Degree']
        choice = form_data.get('Choice_of_Coeff', '0')
        plot_points = form_data.get('Plot_Points', '1')
        plot_curve = form_data.get('Plot_Curve', '1')

        coeffs = [
            form_data.get('Coeff_a1', '0'),
            form_data.get('Coeff_a2', '0'),
            form_data.get('Coeff_a3', '0'),
            form_data.get('Coeff_a4', '0'),
            form_data.get('Coeff_a6', '0'),
        ]

        if choice == '1':
            coeffs = helpers.generate_random_nonsingular_coeffs(base_field, degree)
            cmd = ['sage', 'scripts/List_Elliptic_Curve_Pts_N_Ordrs.py', base_field, degree, '0']
            cmd.extend(coeffs)
            choice_for_plot = '0'
        else:
            cmd = ['sage', 'scripts/List_Elliptic_Curve_Pts_N_Ordrs.py', base_field, degree, choice]
            cmd.extend(coeffs)
            choice_for_plot = choice

        output, error = _run_managed_command(cmd, '/list_points', timeout=120)

        points_plot = ""
        points_plot_error = ""
        if plot_points == '1':
            try:
                points_plot = helpers.generate_plot_image_base64(
                    base_field,
                    degree,
                    choice_for_plot,
                    coeffs,
                    plot_type='points',
                )
            except Exception as plot_exc:
                points_plot_error = str(plot_exc)

        curve_plot = ""
        curve_plot_error = ""
        if plot_curve == '1':
            try:
                curve_plot = helpers.generate_plot_image_base64(
                    base_field,
                    degree,
                    choice_for_plot,
                    coeffs,
                    plot_type='curve',
                )
            except Exception as plot_exc:
                curve_plot_error = str(plot_exc)

        return helpers.result_fragment(
            output=output,
            error=error,
            plot_points=points_plot,
            plot_points_error=points_plot_error,
            plot_curve=curve_plot,
            plot_curve_error=curve_plot_error,
        )

    except subprocess.TimeoutExpired:
        return helpers.result_fragment(error="Calculation timed out after 120 seconds.")
    except Exception as e:
        return helpers.result_fragment(error=str(e))


@app.route('/point_add', methods=['POST'])
def run_point_add():
    try:
        form_data = request.form.to_dict()
        cmd = _build_point_command('Point_Add.py', form_data, include_second_point=True)
        output, error = _run_managed_command(cmd, '/point_add', timeout=120)
        return helpers.result_fragment(output=output, error=error)

    except subprocess.TimeoutExpired:
        return helpers.result_fragment(error="Calculation timed out after 120 seconds.")
    except Exception as e:
        return helpers.result_fragment(error=str(e))


@app.route('/point_multiply', methods=['POST'])
def run_point_multiply():
    try:
        form_data = request.form.to_dict()
        cmd = _build_point_command('Point_Multiply.py', form_data, include_scalar=True)
        output, error = _run_managed_command(cmd, '/point_multiply', timeout=120)
        return helpers.result_fragment(output=output, error=error)

    except subprocess.TimeoutExpired:
        return helpers.result_fragment(error="Calculation timed out after 120 seconds.")
    except Exception as e:
        return helpers.result_fragment(error=str(e))


@app.route('/point_divide', methods=['POST'])
def run_point_divide():
    try:
        form_data = request.form.to_dict()
        cmd = _build_point_command('Point_Divide.py', form_data, include_scalar=True)
        output, error = _run_managed_command(cmd, '/point_divide', timeout=120)
        return helpers.result_fragment(output=output, error=error)

    except subprocess.TimeoutExpired:
        return helpers.result_fragment(error="Calculation timed out after 120 seconds.")
    except Exception as e:
        return helpers.result_fragment(error=str(e))


@app.route('/point_substract', methods=['POST'])
def run_point_substract():
    try:
        form_data = request.form.to_dict()
        cmd = _build_point_command('Point_Substract.py', form_data, include_second_point=True)
        output, error = _run_managed_command(cmd, '/point_substract', timeout=120)
        return helpers.result_fragment(output=output, error=error)

    except subprocess.TimeoutExpired:
        return helpers.result_fragment(error="Calculation timed out after 120 seconds.")
    except Exception as e:
        return helpers.result_fragment(error=str(e))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
