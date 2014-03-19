from flask import Flask, render_template, redirect, request, flash, session, url_for
import model

@app.route("/")
def index():
	