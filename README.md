# AdModel 🎨

AI-powered virtual model webapp for creating custom advertising models with personalized poses and characteristics.

## Features ✨

- **Create Virtual Models**: Design custom models with specific characteristics
- **Customizable Attributes**: 
  - Gender (Male, Female, Non-Binary, Other)
  - Age range
  - Ethnicity (Caucasian, African, Asian, Hispanic, Middle Eastern, Mixed, Other)
  - Skin color (Fair, Light, Medium, Olive, Tan, Brown, Dark Brown)
  - Hair color (Black, Brown, Blonde, Red, Gray, White, Dyed)
  - Body type (Slim, Athletic, Average, Curvy, Plus Size)
  - Height categories
- **Pose Descriptions**: Describe the exact pose you want for your model
- **Product Integration**: Upload product images to combine with your models
- **Save & Reuse**: Save models for future use with different products
- **Model Management**: View, use, and delete saved models

## Tech Stack 🛠️

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Storage**: JSON file-based storage for models
- **API**: RESTful API architecture

## Installation 📦

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/tejas-fuse/AdModel.git
cd AdModel
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application 🚀

Start the server:
```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the npm script:
```bash
npm start
```

The application will be available at: `http://localhost:8000`

## Usage 📖

### Creating a Virtual Model

1. Open the application in your browser
2. Fill out the "Create Virtual Model" form:
   - Enter a name for your model
   - Select gender, age, ethnicity
   - Choose physical characteristics (skin color, hair color, body type, height)
   - Describe the pose you want
   - Optionally upload a product image
3. Click "Create Virtual Model"
4. Your model will be saved and appear in the "Saved Models" list

### Using a Saved Model

1. Find your saved model in the "Saved Models" section
2. Click "Use with Product"
3. Upload a new product image
4. The system will generate an advertisement preview with your model and product

### Managing Models

- **View**: All saved models are displayed in the "Saved Models" section
- **Delete**: Click the "Delete" button on any model to remove it
- **Reuse**: Use the "Use with Product" button to apply the model to new products

## API Endpoints 🔌

### Health Check
```
GET /api/health
```

### Create Model
```
POST /api/models/create
Content-Type: multipart/form-data

Parameters:
- name (string): Model name
- gender (string): Gender
- age (int): Age
- ethnicity (string): Ethnicity
- skin_color (string): Skin color
- hair_color (string): Hair color
- body_type (string): Body type
- height (string): Height
- pose_description (string): Pose description
- product_image (file, optional): Product image
```

### List Models
```
GET /api/models
```

### Get Model
```
GET /api/models/{model_id}
```

### Delete Model
```
DELETE /api/models/{model_id}
```

### Use Model with Product
```
POST /api/models/{model_id}/use-with-product
Content-Type: multipart/form-data

Parameters:
- product_image (file): Product image
```

## Project Structure 📁

```
AdModel/
├── backend/
│   └── main.py           # FastAPI backend application
├── static/
│   └── index.html        # Frontend web interface
├── uploads/              # Uploaded product images
├── saved_models/         # Saved model configurations
├── requirements.txt      # Python dependencies
├── package.json          # Project metadata
├── .gitignore           # Git ignore rules
└── README.md            # Documentation
```

## Development 💻

### Running in Development Mode

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables auto-reload on code changes.

### Adding New Features

1. Backend changes: Edit `backend/main.py`
2. Frontend changes: Edit `static/index.html`
3. Test your changes locally
4. Commit and push

## Future Enhancements 🚀

- Integration with AI image generation models (Stable Diffusion, DALL-E)
- Real-time model preview generation
- More customization options (facial features, clothing style)
- Export functionality for generated advertisements
- User authentication and multi-user support
- Cloud storage integration
- Advanced pose library
- Batch processing for multiple products

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

MIT License - feel free to use this project for personal or commercial purposes.

## Support 💬

For questions or issues, please open an issue on GitHub.

---

Made with ❤️ for creating amazing virtual advertising models
