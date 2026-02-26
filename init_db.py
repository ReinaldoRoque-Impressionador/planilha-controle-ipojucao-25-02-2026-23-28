# init_db.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from modulos.banco.database import inicializar_banco
inicializar_banco()