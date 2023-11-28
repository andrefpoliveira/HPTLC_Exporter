# HPTLC_Exporter

- [What is HPTLC?](#what-is-hptlc)
- [Motivation and Objectives](#motivation-and-objectives)
- [Project Structure](#project-structure)
    - [User Interface](#user-interface)
    - [HPTLC Reader](#hptlc-reader)  
    - [Excel Writer](#excel-writer)
- [How to Run](#how-to-run)

## What is HPTLC?
High-Performance Thin-Layer Chromatography (HPTLC) is a sophisticated chromatographic technique that separates, identifies, and quantifies various compounds in a mixture.

It offers several advantages, such as:
 - **High Resolution:** It provides better resolution and separation of components compared to traditional Thin-Layer Chromatography (TLC).
 - **Speed:** The technique is relatively quick, allowing for the analysis of multiple samples in a short amount of time.
 - **Sensitivity:** HPTLC is sensitive enough to detect trace amounts of compounds in a sample.
 - **Versatility:** It can be used for various sample types, including pharmaceuticals, food, and environmental samples.
 - **Quantitative analysis:** HPTLC can be used for both qualitative and quantitative analysis of compounds in a sample.
 - **Automation:** Some HPTLC systems offer automation, improving precision and reducing the risk of human error.

## Motivation and Objectives
Instituto Português do Mar e da Atmosfera (IPMA) uses HPTLC in lipid class studies, employing methodologies that have undergone extensive testing. The focus is on enhancing the efficiency of separating fundamental lipid components in micro- and macroalgae, with a special emphasis on glycolipids.

An HPTLC report typically includes detailed information about the experimental procedure, the samples analyzed, and the results obtained. For each sample analyzed, there's a table with the following format:

**Track 1, ID: Organ A1 (x mg/mL)**
<table>
  <thead>
    <tr>
      <th>Peak</th>
      <th>Start Rf</th>
      <th>Start Height</th>
      <th>Max Rf</th>
      <th>Max Height</th>
      <th>Max %</th>
      <th>End Rf</th>
      <th>End Height</th>
      <th>Area</th>
      <th>Area %</th>
      <th>Assigned Substance</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan=11>Peak deleted by operator</td>
    </tr>
    <tr>
        <td>1m</td>
        <td>...</td>
        <td>...</td>
        <td>...</td>
        <td>...</td>
        <td>...</td>
        <td>...</td>
        <td>...</td>
        <td>...</td>
        <td>...</td>
        <td>Substance 1</td>
    </tr>
    <tr>
        <td>2m</td>
        <td>...</td>
        <td>...</td>
        <td>...</td>
        <td>...</td>
        <td>...</td>
        <td>...</td>
        <td>...</td>
        <td>...</td>
        <td>...</td>
        <td>Substance 2</td>
    </tr>
  </tbody>
</table>

After obtaining this report and choosing the tracks that matter, the operator must manually copy the data from the report to a spreadsheet. Although usually only the `Area` field is needed, this task is time-consuming and error-prone. Some reports demonstrated that the operator can spend up to 15 minutes copying data from a single report.

This project aims to automate this process, reducing the time spent by the operator and the risk of human error. The final product should be able to read an HPTLC report and extract the data from the table, saving it to a spreadsheet.

## Project Structure
The project was completely developed in Python. Is divided into three parts: the **User Interface**, the **HPTLC Reader**, and the **Excel Writer**.

### User Interface
The User Interface uses the [Tkinter](https://docs.python.org/3/library/tkinter.html) and [CustomTkinter](https://pypi.org/project/customtkinter/) libraries. It allows the user to:

- Create new projects (choose a name, a folder, number of samples and groups)
- Delete existing projects
- Open existing projects
- Upload an HPTLC report (in PDF format) to a project

### HPTLC Reader
The HPTLC Reader uses the [pypdf](https://pypi.org/project/pypdf/) library. It reads the uploaded HPTLC report and extracts the data from the table. The data is then sent to the [Excel Writer](#excel-writer) to be saved to a spreadsheet.

### Excel Writer
The Excel Writer uses the [openpyxl](https://pypi.org/project/openpyxl/) library. It receives the data from the [HPTLC Reader](#hptlc-reader) and saves it to a spreadsheet. The spreadsheet is saved in the path specified by the user when creating the project.

## How to Run
To run the project, you must have Python 3.6 or higher installed. You can download it [here](https://www.python.org/downloads/).

After installing Python, you must install the project dependencies. To do so, open a terminal and run the following command:

```bash
pip install -r requirements.txt
```

Finally, to run the project, run the following command:

```bash
python hptlc_creator.py
```

If you want to create an executable file, you can use [PyInstaller](https://www.pyinstaller.org/). To do so, run the following command:

```bash
pyinstaller --onefile -w --add-data "favicon.ico;." --add-data="search.png;." --icon="favicon.ico" hptlc_creator.py
```

The executable file will be created in the `dist` folder.
