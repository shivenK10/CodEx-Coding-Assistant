import streamlit as st
from generation_pipeline import generate_code, get_available_templates, get_template_display_names
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Code Generator & Executor", layout="wide")
st.title("🛠️ Multi-Language Code Generator")

# Initialize session state for history
if 'code_history' not in st.session_state:
    st.session_state.code_history = []

# Get available templates and display names
available_templates = get_available_templates()
display_names = get_template_display_names()

# Create options for dropdown (display name -> template key mapping)
dropdown_options = ["Select a code type..."] + [display_names.get(template, template.title()) for template in available_templates]

# Create two columns for main content and history
col1, col2 = st.columns([2, 1])

with col1:
    # Dropdown for selecting code type
    selected_display = st.selectbox(
        "Choose the type of code you want to generate:",
        dropdown_options,
        index=0
    )

    # Show text input only if a valid option is selected
    if selected_display != "Select a code type...":
        # Find the corresponding template key
        selected_template = None
        for template_key, display_name in display_names.items():
            if display_name == selected_display:
                selected_template = template_key
                break
        
        if selected_template:
            # Show appropriate placeholder based on selection
            placeholders = {
                'sql_query': 'e.g., List all students older than 18 from the students table',
                'shell_script': 'e.g., Create a backup of all .txt files in the current directory',
                'python_code': 'e.g., Create a function to calculate fibonacci numbers',
                'java_class': 'e.g., Create a Student class with name, age, and grade properties',
                'javascript_function': 'e.g., Create a function to validate email addresses',
            }

            # Form to allow pressing Enter to submit like a chatbot
            with st.form(key="code_form", clear_on_submit=True):
                specification = st.text_input(
                    label="Enter your specification/requirement:",
                    placeholder=placeholders.get(selected_template, "Enter your specification here...")
                )
                submit = st.form_submit_button(f"Generate {selected_display}")

                if submit:
                    if not specification.strip():
                        st.warning("Please enter a specification before generating code.")
                    else:
                        with st.spinner(f"Generating {selected_display}..."):
                            try:
                                generated_code = generate_code(selected_template, specification)
                                
                                # Add to history
                                history_entry = {
                                    'timestamp': datetime.now(),
                                    'code_type': selected_display,
                                    'template': selected_template,
                                    'specification': specification,
                                    'generated_code': generated_code
                                }
                                st.session_state.code_history.insert(0, history_entry)  # Add to beginning
                                
                                # Display the generated code
                                st.subheader(f"Generated {selected_display}")
                                
                                # Determine language for syntax highlighting
                                language_mapping = {
                                    'sql_query': 'sql',
                                    'shell_script': 'bash',
                                    'python_code': 'python',
                                    'java_class': 'java',
                                    'javascript_function': 'javascript',
                                }
                                code_language = language_mapping.get(selected_template, 'text')
                                st.code(generated_code, language=code_language)

                                # Special handling for SQL queries
                                if selected_template == 'sql_query':
                                    st.subheader("Execute SQL Query")
                                    st.info(
                                        "To execute this SQL query, you would need to connect to a database. "
                                        "The query above can be copied and run in your preferred database management tool."
                                    )
                            except Exception as e:
                                st.error(f"An error occurred while generating code: {str(e)}")

with col2:
    st.header("📝 Session History")
    
    # Clear history button
    if st.button("🗑️ Clear History"):
        st.session_state.code_history = []
        st.rerun()
    
    # Display history
    if st.session_state.code_history:
        st.write(f"Total generations: {len(st.session_state.code_history)}")
        
        # Show recent generations
        for i, entry in enumerate(st.session_state.code_history[:10]):  # Show last 10
            with st.expander(f"{entry['code_type']} - {entry['timestamp'].strftime('%H:%M:%S')}"):
                st.write(f"**Specification:** {entry['specification']}")
                st.write(f"**Generated at:** {entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Language mapping for syntax highlighting
                language_mapping = {
                    'sql_query': 'sql',
                    'shell_script': 'bash',
                    'python_code': 'python',
                    'java_class': 'java',
                    'javascript_function': 'javascript',
                }
                code_language = language_mapping.get(entry['template'], 'text')
                st.code(entry['generated_code'], language=code_language)
                
                # Button to reuse this specification
                if st.button(f"Reuse Specification", key=f"reuse_{i}"):
                    # You can add logic here to populate the form with this specification
                    st.info("To reuse this specification, copy the text above and paste it in the main form.")
        
        if len(st.session_state.code_history) > 10:
            st.write(f"... and {len(st.session_state.code_history) - 10} more")
    else:
        st.write("No code generated yet. Start by selecting a code type and entering your specification.")

# Sidebar with information
with st.sidebar:
    st.header("📖 About")
    st.write("""
    This application generates code in multiple programming languages and formats based on your specifications.
    
    **Supported Code Types:**
    - SQL Queries
    - Shell Scripts
    - Python Code
    - Java Classes
    - JavaScript Functions
    """)
    
    st.header("🔧 How to Use")
    st.write("""
    1. Select the type of code you want to generate from the dropdown
    2. Enter your specification in the text input
    3. Press Enter or click the Generate button
    4. View your generation history in the right panel
    5. Copy the generated code or reuse previous specifications
    """)
    
    st.header("💡 Tips")
    st.write("""
    - Be specific in your requirements
    - For SQL queries, mention table names and column requirements
    - Use the history panel to track your previous generations
    - Clear history when needed to start fresh
    """)
    
    st.header("📊 Session Stats")
    if st.session_state.code_history:
        # Count by code type
        code_type_counts = {}
        for entry in st.session_state.code_history:
            code_type = entry['code_type']
            code_type_counts[code_type] = code_type_counts.get(code_type, 0) + 1
        
        st.write("**Generations by type:**")
        for code_type, count in code_type_counts.items():
            st.write(f"- {code_type}: {count}")
    else:
        st.write("No statistics available yet.")