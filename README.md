# Sistema de Procesamiento de Compras - Pipeline CI/CD

## Descripción
Este repositorio contiene el sistema desarrollado para el procesamiento de compras de supermercado. El proyecto está estructurado utilizando scripts modulares de Python (`.py`), sentando las bases para buenas prácticas de MLOps y desarrollo escalable. 

El objetivo principal de este repositorio es demostrar la implementación de un flujo de trabajo basado en Integración Continua (CI) utilizando Git, GitHub y GitHub Actions, validando cambios mediante Pull Requests y pruebas automatizadas.

## Estructura del Proyecto
- `compras.py`: Contiene la lógica principal de procesamiento, cálculo de importes y ordenamiento.
- `tests/test_compras.py`: Suite de pruebas unitarias implementadas con `pytest` que validan cálculos, manejo de datos y lógica de negocio.
- `.github/workflows/ci.yml`: Archivo de configuración de la pipeline de GitHub Actions.
- `requirements.txt`: Dependencias necesarias para ejecutar el proyecto.

## Requisitos Previos
- Python 3.11 o superior.
- Git.

## Instalación
Para correr este proyecto localmente, seguí estos pasos:

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/Maximo-Verdondoni/supermercado-ci.git
   cd supermercado-ci
   ```

2. (Opcional pero recomendado) Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   # En Linux/Mac:
   source venv/bin/activate  
   # En Windows:
   venv\Scripts\activate
   ```

3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución de Pruebas Automatizadas
Este proyecto utiliza `pytest` para garantizar el correcto funcionamiento de las funciones principales. Para correr la suite de pruebas localmente, ejecutar:

```bash
pytest tests/ -v --tb=short
```

## Flujo de Trabajo e Integración Continua (CI)
El proyecto cuenta con un pipeline de CI configurado mediante **GitHub Actions**. El flujo de trabajo establecido requiere el uso de ramas secundarias y Pull Requests (PRs). No se admiten *pushes* directos a la rama principal.

Cada vez que se abre un PR hacia la rama `main`, el pipeline ejecuta automáticamente:
1. Checkout del código fuente.
2. Configuración del entorno con Python 3.11.
3. Instalación de dependencias.
4. Ejecución obligatoria de los unit tests.

### Políticas de Protección
La rama `main` se encuentra protegida mediante *Rulesets* estrictos:
- Se requiere revisión mediante Pull Request.
- Se bloquean *force pushes*.
- **Status Checks requeridos:** Es obligatorio que el pipeline de pruebas (`Ejecutar Tests`) finalice de manera exitosa (verde) para habilitar el botón de Merge.

---
**Autor:** Maximo Verdondoni  
**Institución:** Universidad Austral
