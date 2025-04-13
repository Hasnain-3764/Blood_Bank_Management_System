from app import create_app
import base64
from flask import Response

app = create_app()

@app.route('/base64logo')
def base64logo():
    with open("app/static/images/logo.png", "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode('utf-8')
    return Response(f"data:image/png;base64,{encoded}", mimetype='text/plain')

if __name__ == "__main__":
    app.run(debug=True)
