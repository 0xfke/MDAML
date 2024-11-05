# Malware Analysis Web Application

![Project Banner](Image/Staticw.png)

Malware Detection and Analysis using Machine Learning WebApp is a robust tool designed to provide users with an intuitive interface for analyzing and detecting malware in various file formats. This web app leverages both static analysis through the API and advanced machine learning techniques to ensure comprehensive threat assessment. MDAML is created to address the need for an accessible and user-friendly platform that enables efficient malware analysis for files, URLs, and executables.

## Table of Contents
- [Static Analysis using API](#static-analysis-using-api)
- [Machine Learning-Based Detection](#machine-learning-based-detection)
- [Contributing](#contributing)
- [License](#license)



# Static Analysis using API
- [Static Analysis using API](#static-analysis-using-api)
- [Technologies Used](#technologies-used)
- [File Types Supported](#file-types-supported)
- [DEMO](#demo)
  
- Allows quick, static analysis of files, URLs, and hashes by leveraging VirusTotal’s extensive threat intelligence database.
- This tool integrates two key methods to detect potential threats, providing users with a comprehensive approach to assess security risks.

## Static Analysis using API

The **Static Analysis using API** component provides a fast and effective way to analyze files, URLs, and hashes by leveraging the VirusTotal API. This feature allows users to submit files or URLs and receive detailed threat intelligence, enhancing their ability to quickly identify potential security risks.

---

### Technologies Used

This module uses the following technologies:

- **Flask**: A micro web framework to build the web interface and handle user requests.
- **VirusTotal API**: Provides access to a comprehensive database of known malware signatures and threat intelligence.
- **Python**: The core programming language used for handling file processing, API requests, and responses.
- **Jinja2**: A templating engine used to render HTML templates and display results.

---

### File Types Supported

The tool supports the following file types for static analysis:

- **Executable files**: `.exe`, `.dll`
- **Archive files**: `.zip`, `.tar`
- **Other supported formats**: Files or URLs compatible with VirusTotal API

---

### DEMO

Below is a quick walkthrough demonstrating the **Static Analysis using API** feature in action.

**Upload Page**  
![Upload Page](path/to/upload_page_image.png)  
*Description: A user selects a file from their local directory for analysis.*

**Result Page**  
![Result Page](path/to/result_page_image.png)  
*Description: Analysis results showing threat intelligence based on VirusTotal’s database.*

> **Video Demo**  
> For a more detailed demonstration, watch the video below:  
> [![Watch the Demo](path/to/video_thumbnail.png)](link_to_video)

---

### How It Works

1. **User Input**: The user uploads a file or provides a URL for analysis.
2. **VirusTotal API Integration**: The application sends the file or URL to VirusTotal's API to fetch any associated threat intelligence data.
3. **Result Display**: The retrieved information is processed and displayed on the results page, which includes:
    - **Scan Date**: Date of the last scan for the submitted file/URL.
    - **Detection Ratio**: Ratio of the VirusTotal engines that detected a threat.
    - **Detailed Results**: A breakdown of results from different scanning engines.

---

### Benefits of Static Analysis using API

- **Quick Detection**: Allows immediate scanning using a reliable external threat database.
- **Automated Insights**: Fetches relevant intelligence data without requiring manual lookup.
- **Comprehensive Detection**: Aggregates results from multiple sources to improve detection accuracy.

This tool integrates two key methods to detect potential threats, providing users with a comprehensive approach to assess security risks.

---

**Note**: The VirusTotal API has rate limits, so depending on usage, some requests may experience throttling or delayed responses. Refer to the [VirusTotal API documentation](https://developers.virustotal.com/) for more details on rate limits and usage policies.

---




# Machine Learning-Based Detection
- [Machine Learning-Based Detection](#machine-learning-based-detection)
- [Technologies Used](#technologies-used)
- [Feature Selection and Model Training](#feature-selection-and-model-training)
- [File Types Supported](#file-types-supported)
- [DEMO](#demo)
- Focused on executable files (.exe and .dll), using machine learning and feature extraction to identify malicious behavior.

## Technologies Used

- Python
- Flask
- scikit-learn
- pandas
- pefile
- Joblib

## Feature Selection and Model Training

### Selection of Features According to Their Importances

Using a Random Forest Classifier, we evaluated the importance of different features to identify the most significant ones for malware detection. By filtering the features based on their importances, we set a threshold to select only the most relevant features for training our model. This approach enhances the model's efficiency and accuracy.
### Before Selection of Features According to Their Importances
![Feature Importances](Image/bar1.png) 

### After Selection of Features According to Their Importances

![Feature Importances](Image/bar2.png)


### Training a New Model Based on Important Features

After selecting the important features, we trained a new model, which yielded the following classification metrics:

| Class    | Precision | Recall | F1-Score | Support |
|----------|-----------|--------|----------|---------|
| Benign   | 1.00      | 0.97   | 0.98     | 1003    |
| Malware  | 0.99      | 1.00   | 0.99     | 2920    |
| **Accuracy**     | **0.99**  |        |          | **3923**    |
| Macro Avg| 0.99      | 0.98   | 0.99     | 3923    |
| Weighted Avg| 0.99   | 0.99   | 0.99     | 3923    |

**Training Scores:**  
The average training score is approximately 99.13%.

**Validation Scores:**  
The average validation score is around 98.63%.

The results demonstrate high performance for both training and validation sets, with only a slight discrepancy of 0.51%.

### Analysis

- **No Overfitting:** The close alignment of training and validation scores indicates that the model is likely not overfitting. In cases of significant overfitting, we would expect a higher training score compared to the validation score.
  
- **Slight Underfitting Possibility:** While the validation score is marginally lower than the training score, indicating a slight potential for underfitting, the difference is minimal.

### Learning Curves

To assess the model's performance over different training set sizes, we generated learning curves. These curves help visualize how the model's accuracy evolves as more training data is added.

![Learning Curves](Image/bar3.png) 

### Training and Validation Scores by Training Set Size

The bar chart below displays the average training and validation scores along with their standard deviations across various training set sizes.

![Training and Validation Scores](Image/bar4.png)

---

By analyzing these scores and visualizations, we gain insight into the model's learning behavior and can make informed decisions for further improvements.




## DEMO



## File Types Supported

    Executable files: .exe, .dll
    Archive files: .zip, .tar

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

    Fork the repository.
    Create a new branch (git checkout -b feature/YourFeature).
    Make your changes and commit them (git commit -m 'Add some feature').
    Push to the branch (git push origin feature/YourFeature).
    Open a pull request.

License

This project is licensed under the MIT License. See the LICENSE file for details.
