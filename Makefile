# --- Variables de configuración ---
PYTHON_SYS = python3
VENV = venv
BIN = $(VENV)/bin
DEPS_STAMP = $(VENV)/.deps_installed

# Ejecutables dentro del entorno virtual
PYTHON = $(BIN)/python
PIP = $(BIN)/pip
MYPY = $(BIN)/mypy
FLAKE8 = $(BIN)/flake8

# Archivos del proyecto
MAIN = a_maze_ing.py
CONFIG = config.txt

# Flags de MyPy exigidos por el PDF
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports \
             --disallow-untyped-defs --check-untyped-defs

# Colores para la terminal
GREEN = \033[0;32m
CYAN  = \033[0;36m
NC    = \033[0m

.PHONY: all install run debug clean lint lint-strict

all: run

# 1. Instalar: crea el venv si no existe e instala dependencias solo cuando
# cambian archivos relevantes (evita reinstalar en cada make install).
install: $(DEPS_STAMP)

$(BIN)/python:
	@echo "$(CYAN)Verificando entorno virtual...$(NC)"
	@if [ ! -d "$(VENV)" ]; then \
		$(PYTHON_SYS) -m venv $(VENV); \
		echo "$(GREEN)Entorno virtual creado en la carpeta /$(VENV)$(NC)"; \
	fi

$(DEPS_STAMP): requirements.txt Makefile | $(BIN)/python
	@echo "$(CYAN)Instalando/Actualizando dependencias...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@touch $(DEPS_STAMP)

# 2. Ejecutar el programa (usando el python del venv)
run: install
	@if [ ! -f "$(BIN)/python" ]; then echo "Error: Ejecuta 'make install' primero."; exit 1; fi
	$(PYTHON) $(MAIN) $(CONFIG)

# 3. Modo debug con pdb
debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

# 4. Limpieza total (incluye borrar el venv)
clean:
	@echo "$(CYAN)Limpiando archivos temporales y entorno virtual...$(NC)"
	find . -name "*.txt" ! -name "config.txt" ! -name "requirements.txt" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf $(VENV)
	@echo "$(GREEN)Limpieza completada.$(NC)"

# 5. Linter obligatorio
lint:
	@echo "Executing flake8..."
	$(FLAKE8) . --exclude=$(VENV)
	@echo "Executing mypy..."
	$(MYPY) . $(MYPY_FLAGS) --exclude $(VENV)

# 6. Linter estricto
lint-strict:
	$(FLAKE8) . --exclude=$(VENV)
	$(MYPY) . --strict --exclude $(VENV)