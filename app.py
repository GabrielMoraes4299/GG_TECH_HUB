from flask import Flask, render_template, request, redirect, session, jsonify

app = Flask(__name__)

app.secret_key = "capivara"

app.run(debug=True)