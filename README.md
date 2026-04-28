# 🐠 Smart Aquarium Monitor (AI Vision Agent)

An intelligent monitoring system that uses **Computer Vision** and **Local LLMs** to track the health and ecosystem of a 112L aquarium.

## 🌟 Overview
Monitoring an aquarium usually requires manual observation. This agent automates the process by "looking" at the tank through a camera, identifying species, observing plant growth, and logging environmental changes. It turns visual data into actionable insights without sending any data to the cloud, ensuring total privacy.

## 🚀 Key Features
* **AI-Powered Vision:** Uses **Ollama Vision** models to analyze images and describe the state of the aquarium.
* **Automated Species Tracking:** Identifies fish behavior and counts (e.g., Neon Tetras, Corydoras) to ensure no one is missing.
* **Flora Analysis:** Monitors plant health and algae growth levels over time.
* **Health Logging:** Automatically saves daily reports into a structured **JSON database** or **Google Sheets**.
* **Privacy First:** All image processing happens locally on your machine—no external cameras or cloud AI services are required.

---

## 🛠️ Technical Implementation

This project is a sophisticated implementation of **Vision-Language Models (VLM)** and automated data pipelines.

### Core Architecture:
1. **Visual Capture:** High-resolution snapshots are taken via a connected camera module.
2. **Local Vision Inference:** The agent sends the image to a local **Llama 3 Vision** or **Moondream** model running via Ollama.
3. **Contextual Analysis:** The model is prompted with a specific domain-expert persona (Aquarist) to extract metrics like water clarity, fish vitality, and plant coloration.
4. **Data Synchronization:** Extracted insights are parsed into JSON and appended to a **Google Sheets** dashboard for long-term trend visualization.

### Technical Stack:
* **Language:** Python 3.12+
* **AI Engine:** **Ollama** (Local VLM)
* **Storage:** Google Sheets API & Local JSON
* **Dev Environment:** **Neovim** (Lua-based configuration)
* **Version Control:** Git (Hosted on GitHub)

---

## 📚 Resources & Presentations
* **Conceptual Framework:** [Building Autonomous AI Agents (SlideShare)](https://www.slideshare.net/slideshow/building-an-autonomous-ai-agent-to-automate-spotify-playlist-updates-from-lrt-opus/287226278)

---
*Developed to bridge the gap between hobbyist fishkeeping and modern AI engineering.*
