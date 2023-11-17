import logging
import traceback

import flask
from replit import db

app = flask.Flask(__name__)


@app.errorhandler(500)
def internal_server_error(e: str):
  
  return flask.jsonify(error=str(e)), 500



@app.route('/', methods=['GET', 'POST'])
def cadastroContatos():
  try:
    
    contatos = db.get('contatos', {})
    print(contatos)

    if flask.request.method == "POST":
      email = flask.request.form['email']
      contatos[email] = {
          'nome': flask.request.form['nome'],
          'email': email,
          'telefone': flask.request.form['telefone'],
          'assunto': flask.request.form['assunto'],
          'mensagem': flask.request.form['mensagem'],
          'opcao_resposta': flask.request.form.getlist('resposta')
      }
      db['contatos'] = contatos
      return flask.render_template('contatos.html', contatos=contatos)
  
  except Exception as e:
    
    logging.exception('failed to database')
    flask.flash(f"Failed to save data: {str(e)}")

  return flask.render_template('contatos.html', contatos=contatos)


@app.route('/limparBanco', methods=['POST'])
def limparBanco():
  
  try:
    
    contatos = db.get('contatos', {})

    if contatos is not None and contatos != {}:
      
      del db["contatos"]
    return flask.redirect(flask.url_for('cadastroContatos'))
    
  except Exception as e:
    
    logging.exception(e)
    return flask.render_template('contatos.html', contatos={})
    
app.run('0.0.0.0')