import os
import papermill as pm
import nbformat
import tempfile   

NOTEBOOKS_DIR = "notebooks"
NOTEBOOK_NAME = os.environ.get("NOTEBOOK_NAME")  # Optional: passed in via env var

def log_outputs(notebook_path):
    with tempfile.NamedTemporaryFile(suffix=".ipynb", delete=False) as tmp:
        pm.execute_notebook(notebook_path, tmp.name)

        with open(tmp.name, "r") as f:
            nb = nbformat.read(f, as_version=4)
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    for output in cell.get('outputs', []):
                        if output.output_type == 'stream':
                            print(f">>> {output.text.strip()}")
                        elif output.output_type == 'execute_result':
                            print(f">>> {output['data'].get('text/plain', '').strip()}")
                        elif output.output_type == 'error':
                            print(f"!!! Error: {output['ename']}: {output['evalue']}")

def run():
    if NOTEBOOK_NAME:
        # Run a specific notebook
        full_path = os.path.join(NOTEBOOKS_DIR, NOTEBOOK_NAME)
        if not os.path.exists(full_path):
            print(f"Notebook '{NOTEBOOK_NAME}' not found.")
            return
        print(f"\n========== Running notebook: {NOTEBOOK_NAME} ==========\n")
        log_outputs(full_path)
    else:
        # Run all notebooks
        notebooks = sorted([
            os.path.join(NOTEBOOKS_DIR, f)
            for f in os.listdir(NOTEBOOKS_DIR)
            if f.endswith(".ipynb")
        ])

        if not notebooks:
            print("No notebooks found to run.")
            return

        for notebook in notebooks:
            try:
                print(f"\n========== Running notebook: {notebook} ==========\n")
                log_outputs(notebook)
            except Exception as e:
                print(f"!!! Error running notebook {notebook}: {e}")

if __name__ == "__main__":
    run()
