import base64
import json
import os
import subprocess
import tempfile

from markupsafe import escape


_SAGE_PLOT_SNIPPET = r'''
import json
import base64
import os
import sys
import tempfile
from sage.all import *

payload = json.loads(sys.stdin.read())
p = Integer(payload["base_field"])
n = Integer(payload["degree"])
choice = payload["choice"]
plot_type = payload["plot_type"]

F = GF(p ** n, 'a')

if choice == "0":
    coeffs = [F(c) for c in payload["coeffs"]]
    E = EllipticCurve(F, coeffs)
else:
    # Retry a few times to avoid singular random curves.
    E = None
    for _ in range(20):
        coeffs = [F.random_element() for _ in range(5)]
        try:
            E = EllipticCurve(F, coeffs)
            break
        except Exception:
            continue
    if E is None:
        raise ValueError("Unable to generate a valid random elliptic curve for plotting.")

def _elem_to_int(v):
    # Map finite field elements to deterministic integer representatives.
    if hasattr(v, 'integer_representation'):
        return int(ZZ(v.integer_representation()))
    try:
        return int(ZZ(v))
    except Exception:
        return int(ZZ(v.lift()))

if plot_type == "curve":
    # Plot as a real implicit curve for degree 1.
    a1, a2, a3, a4, a6 = [_elem_to_int(c) for c in E.a_invariants()]
    x, y = var('x y')
    span = min(max(int(p), 10), 200)
    curve_eq = (y^2 + a1*x*y + a3*y) - (x^3 + a2*x^2 + a4*x + a6)
    plot_obj = implicit_plot(
        curve_eq,
        (x, -span, span),
        (y, -span, span),
        color='navy',
        figsize=6,
    )
elif plot_type == "points":
    pts = []
    for P in E.points():
        if P.is_zero():
            continue
        pts.append((_elem_to_int(P[0]), _elem_to_int(P[1])))

    if pts:
        plot_obj = list_plot(pts, color='crimson', marker='o', size=36, figsize=6)
    else:
        plot_obj = text('No finite points to plot', (0, 0), color='black')
else:
    raise ValueError("Unknown plot type requested.")

tmp_path = None
try:
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        tmp_path = tmp_file.name

    plot_obj.save(filename=tmp_path)
    with open(tmp_path, 'rb') as png_file:
        print(base64.b64encode(png_file.read()).decode('ascii'))
finally:
    if tmp_path and os.path.exists(tmp_path):
        os.remove(tmp_path)
'''


_SAGE_RANDOM_COEFFS_SNIPPET = r'''
import json
import sys
from sage.all import *

payload = json.loads(sys.stdin.read())
p = Integer(payload["base_field"])
n = Integer(payload["degree"])
attempts = Integer(payload["attempts"])

F = GF(p ** n, 'a')

for _ in range(attempts):
    coeffs = [F.random_element() for _ in range(5)]
    try:
        EllipticCurve(F, coeffs)
        print(json.dumps([str(c) for c in coeffs]))
        break
    except Exception:
        continue
else:
    raise ValueError("Unable to generate non-singular random coefficients.")
'''


def get_template_styles_dir():
    return os.path.join(os.path.dirname(__file__), "templates", "styles")


def generate_plot_base64(base_field, degree, choice, coeffs):
    if str(degree) != '1':
        raise ValueError("Plotting is only supported for degree 1.")

    payload = {
        "base_field": base_field,
        "degree": degree,
        "choice": choice,
        "coeffs": coeffs,
        "plot_type": "curve",
    }

    result = subprocess.run(
        ['sage', '-c', _SAGE_PLOT_SNIPPET],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=120,
    )

    if result.returncode != 0:
        error_message = (result.stderr or result.stdout or "Unknown plotting error").strip()
        raise RuntimeError(error_message)

    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not lines:
        raise RuntimeError("No plot output was produced by SageMath.")

    return lines[-1]


def generate_plot_image_base64(base_field, degree, choice, coeffs, plot_type):
    if str(degree) != '1':
        raise ValueError("Plotting is only supported for degree 1.")

    payload = {
        "base_field": base_field,
        "degree": degree,
        "choice": choice,
        "coeffs": coeffs,
        "plot_type": plot_type,
    }

    result = subprocess.run(
        ['sage', '-c', _SAGE_PLOT_SNIPPET],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=120,
    )

    if result.returncode != 0:
        error_message = (result.stderr or result.stdout or "Unknown plotting error").strip()
        raise RuntimeError(error_message)

    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not lines:
        raise RuntimeError("No plot output was produced by SageMath.")

    return lines[-1]


def generate_random_nonsingular_coeffs(base_field, degree, attempts=50):
    payload = {
        "base_field": base_field,
        "degree": degree,
        "attempts": attempts,
    }

    result = subprocess.run(
        ['sage', '-c', _SAGE_RANDOM_COEFFS_SNIPPET],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=120,
    )

    if result.returncode != 0:
        error_message = (result.stderr or result.stdout or "Unknown random coefficient error").strip()
        raise RuntimeError(error_message)

    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not lines:
        raise RuntimeError("No random coefficients were produced by SageMath.")

    return json.loads(lines[-1])


def result_fragment(
    output="",
    error="",
    plot_points="",
    plot_points_error="",
    plot_curve="",
    plot_curve_error="",
):
    """Return a tiny HTML fragment parsed by home.html JS."""
    safe_output = escape(output or "")
    safe_error = escape(error or "")
    safe_plot_points = escape(plot_points or "")
    safe_plot_points_error = escape(plot_points_error or "")
    safe_plot_curve = escape(plot_curve or "")
    safe_plot_curve_error = escape(plot_curve_error or "")
    return (
        f"<h3>Output:</h3><pre>{safe_output}</pre>"
        f"<h3>Error:</h3><pre>{safe_error}</pre>"
        f"<h3>Plot Points:</h3><pre>{safe_plot_points}</pre>"
        f"<h3>Plot Points Error:</h3><pre>{safe_plot_points_error}</pre>"
        f"<h3>Plot Curve:</h3><pre>{safe_plot_curve}</pre>"
        f"<h3>Plot Curve Error:</h3><pre>{safe_plot_curve_error}</pre>"
    )
