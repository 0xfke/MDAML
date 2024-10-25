from flask import Flask, request, jsonify, render_template
import joblib
import os
import pandas as pd
import pefile
import math

app = Flask(__name__)

# Load the trained model
model = joblib.load('malware_detection_model.pkl')

# Create a folder to save uploaded files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'dll', 'exe'}
# Helper function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Function to calculate entropy of a section
def calculate_entropy(data):
    if not data:
        return 0
    entropy = 0
    for x in range(256):
        p_x = float(data.count(bytes([x]))) / len(data)  # Use bytes([x]) instead of chr(x)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy
def extract_features(file_path):
    pe = pefile.PE(file_path)
    
    # DOS Header features
    dos_header = {
        'e_magic': pe.DOS_HEADER.e_magic,
        'e_cblp': pe.DOS_HEADER.e_cblp,
        'e_cp': pe.DOS_HEADER.e_cp,
        'e_crlc': pe.DOS_HEADER.e_crlc,
        'e_cparhdr': pe.DOS_HEADER.e_cparhdr,
        'e_minalloc': pe.DOS_HEADER.e_minalloc,
        'e_maxalloc': pe.DOS_HEADER.e_maxalloc,
        'e_ss': pe.DOS_HEADER.e_ss,
        'e_sp': pe.DOS_HEADER.e_sp,
        'e_csum': pe.DOS_HEADER.e_csum,
        'e_ip': pe.DOS_HEADER.e_ip,
        'e_cs': pe.DOS_HEADER.e_cs,
        'e_lfarlc': pe.DOS_HEADER.e_lfarlc,
        'e_ovno': pe.DOS_HEADER.e_ovno,
        'e_oemid': pe.DOS_HEADER.e_oemid,
        'e_oeminfo': pe.DOS_HEADER.e_oeminfo,
        'e_lfanew': pe.DOS_HEADER.e_lfanew
    }

    # File Header features
    file_header = {
        'Machine': pe.FILE_HEADER.Machine,
        'NumberOfSections': pe.FILE_HEADER.NumberOfSections,
        'TimeDateStamp': pe.FILE_HEADER.TimeDateStamp,
        'PointerToSymbolTable': pe.FILE_HEADER.PointerToSymbolTable,
        'NumberOfSymbols': pe.FILE_HEADER.NumberOfSymbols,
        'SizeOfOptionalHeader': pe.FILE_HEADER.SizeOfOptionalHeader,
        'Characteristics': pe.FILE_HEADER.Characteristics
    }

    # Optional Header features
    optional_header = {
        'Magic': pe.OPTIONAL_HEADER.Magic,
        'MajorLinkerVersion': pe.OPTIONAL_HEADER.MajorLinkerVersion,
        'MinorLinkerVersion': pe.OPTIONAL_HEADER.MinorLinkerVersion,
        'SizeOfCode': pe.OPTIONAL_HEADER.SizeOfCode,
        'SizeOfInitializedData': pe.OPTIONAL_HEADER.SizeOfInitializedData,
        'SizeOfUninitializedData': pe.OPTIONAL_HEADER.SizeOfUninitializedData,
        'AddressOfEntryPoint': pe.OPTIONAL_HEADER.AddressOfEntryPoint,
        'BaseOfCode': pe.OPTIONAL_HEADER.BaseOfCode,
        'ImageBase': pe.OPTIONAL_HEADER.ImageBase,
        'SectionAlignment': pe.OPTIONAL_HEADER.SectionAlignment,
        'FileAlignment': pe.OPTIONAL_HEADER.FileAlignment,
        'MajorOperatingSystemVersion': pe.OPTIONAL_HEADER.MajorOperatingSystemVersion,
        'MinorOperatingSystemVersion': pe.OPTIONAL_HEADER.MinorOperatingSystemVersion,
        'MajorImageVersion': pe.OPTIONAL_HEADER.MajorImageVersion,
        'MinorImageVersion': pe.OPTIONAL_HEADER.MinorImageVersion,
        'MajorSubsystemVersion': pe.OPTIONAL_HEADER.MajorSubsystemVersion,
        'MinorSubsystemVersion': pe.OPTIONAL_HEADER.MinorSubsystemVersion,
        'SizeOfHeaders': pe.OPTIONAL_HEADER.SizeOfHeaders,
        'CheckSum': pe.OPTIONAL_HEADER.CheckSum,
        'SizeOfImage': pe.OPTIONAL_HEADER.SizeOfImage,
        'Subsystem': pe.OPTIONAL_HEADER.Subsystem,
        'DllCharacteristics': pe.OPTIONAL_HEADER.DllCharacteristics,
        'SizeOfStackReserve': pe.OPTIONAL_HEADER.SizeOfStackReserve,
        'SizeOfStackCommit': pe.OPTIONAL_HEADER.SizeOfStackCommit,
        'SizeOfHeapReserve': pe.OPTIONAL_HEADER.SizeOfHeapReserve,
        'SizeOfHeapCommit': pe.OPTIONAL_HEADER.SizeOfHeapCommit,
        'LoaderFlags': pe.OPTIONAL_HEADER.LoaderFlags,
        'NumberOfRvaAndSizes': pe.OPTIONAL_HEADER.NumberOfRvaAndSizes
    }

    # 0 is Placeholder for the featurs that i didn't find ways to extract from the given file header.
    # Additional features based on the original column list
    additional_features = {
        'SuspiciousImportFunctions': 0,
        'SuspiciousNameSection': 0,
        'SectionsLength': len(pe.sections),
        'SectionMinEntropy': None,
        'SectionMaxEntropy': None,
        'SectionMinRawsize': None,
        'SectionMaxRawsize': None,
        'SectionMinVirtualsize': None,
        'SectionMaxVirtualsize': None,
        'SectionMaxPhysical': None,
        'SectionMinPhysical': None,
        'SectionMaxVirtual': 0,            
        'SectionMinVirtual': 0,            
        'SectionMaxPointerData': None,
        'SectionMinPointerData': None,
        'SectionMaxChar': 0,               
        'SectionMainChar': 0,
        'DirectoryEntryImport': 0,
        'DirectoryEntryImportSize': 0,
        'DirectoryEntryExport': 0,
        'ImageDirectoryEntryExport': 0,
        'ImageDirectoryEntryImport': 0,
        'ImageDirectoryEntryResource': 0,
        'ImageDirectoryEntryException': 0,
        'ImageDirectoryEntrySecurity': 0,
    }
    # Check for suspicious import functions
    suspicious_imports = ['VirtualAlloc', 'CreateRemoteThread']
    if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            for imp in entry.imports:
                if imp.name and any(suspicious in imp.name.decode('utf-8', errors='ignore') for suspicious in suspicious_imports):
                 additional_features['SuspiciousImportFunctions'] += 1

    # Check for suspicious section names
    suspicious_section_names = ['UPX', '.textbss', '.evil']
    for section in pe.sections:
        section_name = section.Name.decode('utf-8', errors='ignore').strip('\x00')
        if section_name in suspicious_section_names:
            additional_features['SuspiciousNameSection'] += 1

    # Calculate section entropy, raw size, and virtual size
    entropies = []
    raw_sizes = []
    virtual_sizes = []
    for section in pe.sections:
        entropy = calculate_entropy(section.get_data())
        entropies.append(entropy)
        raw_sizes.append(section.SizeOfRawData)
        virtual_sizes.append(section.Misc_VirtualSize)

    if entropies:
        additional_features['SectionMinEntropy'] = min(entropies)
        additional_features['SectionMaxEntropy'] = max(entropies)
    if raw_sizes:
        additional_features['SectionMinRawsize'] = min(raw_sizes)
        additional_features['SectionMaxRawsize'] = max(raw_sizes)
    if virtual_sizes:
        additional_features['SectionMinVirtualsize'] = min(virtual_sizes)
        additional_features['SectionMaxVirtualsize'] = max(virtual_sizes)

    # Directory Entry Import and Export
    if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
        additional_features['DirectoryEntryImport'] = 1
        additional_features['DirectoryEntryImportSize'] = pe.OPTIONAL_HEADER.DATA_DIRECTORY[1].Size

    if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
        additional_features['DirectoryEntryExport'] = 1
        additional_features['ImageDirectoryEntryExport'] = pe.OPTIONAL_HEADER.DATA_DIRECTORY[0].Size

    # Other directories
    additional_features['ImageDirectoryEntryImport'] = pe.OPTIONAL_HEADER.DATA_DIRECTORY[1].Size
    additional_features['ImageDirectoryEntryResource'] = pe.OPTIONAL_HEADER.DATA_DIRECTORY[2].Size
    additional_features['ImageDirectoryEntryException'] = pe.OPTIONAL_HEADER.DATA_DIRECTORY[3].Size
    additional_features['ImageDirectoryEntrySecurity'] = pe.OPTIONAL_HEADER.DATA_DIRECTORY[4].Size



    features = {**dos_header, **file_header, **optional_header, **additional_features}
    return pd.DataFrame([features])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return render_template('index.html', error="No file provided")

    file = request.files['file']
    # Check if the file has a valid extension
    if file.filename == '' or not allowed_file(file.filename):
            return render_template('index.html', error="Unsupported file type. Please upload a .dll or .exe file.")
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Extract features from the uploaded file
    features = extract_features(file_path)
    
    # Predict using the trained model
    prediction = model.predict(features)
    result = 'Malware' if prediction[0] == 1 else 'Safe'
    
    # Render the result on the web page
    return render_template('result.html', result=result)
        # Handle any other errors that occur during processing

if __name__ == '__main__':
    app.run(debug=True)

