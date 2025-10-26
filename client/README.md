# f(unc) - Meme Explainer Frontend

A Next.js React application for explaining memes to different generations using the f(unc) API.

## Color Scheme

- Green: `#024f46`
- Black: `#1a1a1a`
- Off-white: `#ffffeb`

## Features

- **f(unc) branding** in top left corner
- **uncify()** function-style interface with two parameters:
  - `meme`: Text input for the meme topic
  - `generation`: Carousel-style enum selector (boomer, gen-x, millenial, gen-z)
- **Loading animation**: Three bouncing dots while fetching data
- **Results display**:
  - Left side: Meme name, explanation, and sources
  - Right side: YouTube video collage in iframe format

## Getting Started

### Prerequisites

- Node.js 18+
- The backend API running on `http://localhost:8000`

### Installation

Dependencies are already installed. If you need to reinstall:

```bash
npm install
```

### Running the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Building for Production

```bash
npm run build
npm start
```

## API Integration

The app integrates with two backend endpoints:

1. `/explain/explanation` - Fetches meme explanation tailored to generation
2. `/media/videos` - Fetches YouTube videos related to the meme

Configure the API URL in `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project Structure

```
client/
├── app/
│   ├── page.tsx          # Main landing page
│   ├── layout.tsx        # Root layout
│   └── globals.css       # Global styles
├── components/
│   ├── LoadingDots.tsx   # Loading animation
│   ├── ResultsDisplay.tsx # Meme explanation display
│   └── VideoCollage.tsx  # YouTube video grid
└── lib/
    ├── api.ts            # API client functions
    └── types.ts          # TypeScript interfaces
```

## Usage

1. Enter a meme name in the `meme` input field
2. Click the `generation` button to cycle through different generations
3. Click the submit button `:--)` to fetch results
4. View the explanation on the left and related videos on the right
