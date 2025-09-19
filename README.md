# Software-v2

This repository is a Python-based Trash Sorting Application featuring a graphical user interface (GUI) built with Tkinter.

## Features
- Trash sorting workflow with categorized pages (Main, Location, Type, Weigh)
- Integrated MVC architecture with model data handling
- Full-screen GUI optimized for 1024x600 displays

## Requirements

- Python 3.x
- Tkinter (usually included in standard Python installations)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MuhammadIqbalBaihaqi/Software-v2.git
   cd Software-v2
   ```

2. **(Optional) Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   - If your app has other dependencies in `requirements.txt`, install them:
     ```bash
     pip install -r requirements.txt
     ```
   - If no `requirements.txt` is present, Tkinter is usually included by default.

## Running the Application

To start the Trash Sorting App, run:

```bash
python main_app.py
```

The application will launch in full-screen mode.

## File Structure

- `main_app.py`: Main entry point for the application.
- `views/`: Contains GUI page classes (`MainPage`, `LocationPage`, `TypePage`, `WeighPage`).
- `model.py`: Data model logic for trash sorting.
- Other supporting files and folders.

## Notes

- Ensure all files and folders in the repository are downloaded for the app to work.
- For full functionality, keep `model.py` and the `views` folder in the same directory as `main_app.py`.

## License

This project is licensed under the MIT License.
