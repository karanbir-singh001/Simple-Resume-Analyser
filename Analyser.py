import PyPDF2
import spacy
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def analyze_resume(text):

    doc = nlp(text)
    
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    skills = ['Python', 'Java', 'Machine Learning']  # Example skills
    matched_skills = [token.text for token in doc if token.text in skills]
    
    return entities, matched_skills

def analyze_resume_from_file():
    file_path = filedialog.askopenfilename(title="Select Resume (PDF)")
    if file_path:
        resume_text = extract_text_from_pdf(file_path)
        entities, matched_skills = analyze_resume(resume_text)
        display_results(entities, matched_skills)

def display_results(entities, matched_skills):
    result_window = tk.Toplevel()
    result_window.title("Resume Analysis Results")
    result_window.geometry("500x400")

    entities_str = "\n".join([f"{entity}: {label}" for entity, label in entities])
    skills_str = "\n".join(matched_skills)

    result_text = scrolledtext.ScrolledText(result_window, wrap=tk.WORD)
    result_text.insert(tk.END, f"Entities found in the resume:\n{entities_str}\n\nMatched Skills found in the resume:\n{skills_str}")
    result_text.pack(expand=True, fill="both", padx=10, pady=10)

def main():
    root = tk.Tk()
    root.title("Resume Analyzer")

    analyze_button = tk.Button(root, text="Analyze Resume", command=analyze_resume_from_file)
    analyze_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
