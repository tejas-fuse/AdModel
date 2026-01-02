# AdModel - Quick Start Guide

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tejas-fuse/AdModel.git
   cd AdModel
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Option 1: Using the startup script (Linux/Mac)
```bash
./start.sh
```

### Option 2: Using the startup script (Windows)
```bash
start.bat
```

### Option 3: Manual start
```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 4: Using npm
```bash
npm start
```

## Access the Application

Open your browser and navigate to: **http://localhost:8000**

## Features

### 1. Create Virtual Models
- Fill out the form with model characteristics:
  - **Name**: Give your model a unique name
  - **Gender**: Male, Female, Non-Binary, or Other
  - **Age**: 18-80 years
  - **Ethnicity**: Caucasian, African, Asian, Hispanic, Middle Eastern, Mixed, Other
  - **Skin Color**: Fair, Light, Medium, Olive, Tan, Brown, Dark Brown
  - **Hair Color**: Black, Brown, Blonde, Red, Gray, White, Dyed
  - **Body Type**: Slim, Athletic, Average, Curvy, Plus Size
  - **Height**: Short, Average, or Tall
  - **Pose Description**: Describe the exact pose you want
  - **Product Image** (Optional): Upload a product image

### 2. Save Models for Future Use
- All created models are automatically saved
- Models appear in the "Saved Models" section
- Each model stores all characteristics and configurations

### 3. Use Saved Models with New Products
- Click "Use with Product" on any saved model
- Upload a new product image
- The system generates an advertisement preview

### 4. Manage Models
- View all saved models with their characteristics
- Delete models you no longer need
- Reuse models across multiple products

## API Endpoints

### Health Check
```bash
GET /api/health
```

### Create Model
```bash
POST /api/models/create
Content-Type: multipart/form-data
```

### List All Models
```bash
GET /api/models
```

### Get Specific Model
```bash
GET /api/models/{model_id}
```

### Delete Model
```bash
DELETE /api/models/{model_id}
```

### Use Model with New Product
```bash
POST /api/models/{model_id}/use-with-product
Content-Type: multipart/form-data
```

## Testing the API

```bash
# Health check
curl http://localhost:8000/api/health

# List models
curl http://localhost:8000/api/models

# Get specific model
curl http://localhost:8000/api/models/{model_id}
```

## Project Structure

```
AdModel/
├── backend/
│   ├── __init__.py
│   └── main.py           # FastAPI backend
├── static/
│   └── index.html        # Web interface
├── uploads/              # Product images
├── saved_models/         # Model configurations
├── requirements.txt      # Python dependencies
├── package.json          # Project metadata
├── start.sh             # Linux/Mac startup
├── start.bat            # Windows startup
├── .gitignore           # Git ignore rules
└── README.md            # Documentation
```

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, you can change it:
```bash
python -m uvicorn backend.main:app --port 8080
```

### Dependencies Not Installing
Make sure you have Python 3.8 or higher:
```bash
python --version
```

### Virtual Environment Issues
Create a fresh virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Future Enhancements

- AI image generation integration (Stable Diffusion, DALL-E)
- Real-time model preview
- Export functionality for advertisements
- User authentication
- Cloud storage integration
- Advanced pose library

## Support

For issues or questions, please open an issue on GitHub.
