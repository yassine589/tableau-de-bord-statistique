import os
# Set Streamlit to headless mode to reduce system interactions
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import io

# Try to import statsmodels for Q-Q plot and linear regression, handle if not available
try:
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    statsmodels_available = True
except ImportError:
    statsmodels_available = False

# Page configuration
st.set_page_config(
    page_title="Tableau de Bord Statistique",
    page_icon="📊",
    layout="wide"
)

# CSS styling - Updated .info-box for better readability and to remove empty white rectangles
st.markdown("""
<style>
    .sidebar .sidebar-content {
        background-color: #343a40;
        color: white;
    }
    h1 {
        color: #dc3545;
        text-align: center;
        margin-bottom: 30px;
    }
    h2 {
        color: #2c3e50;
        border-bottom: 2px solid #007bff;
        padding-bottom: 5px;
    }
    .stButton button {
        background-color: #007bff;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #0056b3;
        transform: scale(1.05);
    }
    .feature-list {
        font-size: 18px;
        line-height: 2.0;
        margin: 30px 0;
    }
    .dataframe {
        width: 100%;
    }
    .missing-values-warning {
        background-color: #ff0000;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    .welcome-banner {
        background: linear-gradient(135deg, #007bff 0%, #dc3545 100%);
        color: white;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .welcome-banner h2 {
        color: white;
        border: none;
        margin: 0;
        font-size: 36px;
    }
    .welcome-banner p {
        font-size: 18px;
        margin: 10px 0 20px 0;
    }
    .feature-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    .feature-card i {
        font-size: 40px;
        color: #007bff;
        margin-bottom: 10px;
    }
    .feature-card h4 {
        color: #2c3e50;
        margin: 10px 0;
        font-size: 20px;
    }
    .feature-card p {
        color: #6c757d;
        font-size: 16px;
    }
    .cta-button {
        text-align: center;
        margin-top: 40px;
    }
    .section-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    .info-box {
        background-color: #e9ecef;
        border-left: 5px solid #007bff;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        color: #2c3e50; /* Improved contrast for readability */
    }
    /* Remove empty white rectangles after .info-box */
    .info-box:empty,
    .info-box + div:empty,
    .info-box + div > div:empty {
        display: none !important;
    }
    /* Reduce extra spacing after .info-box */
    .info-box {
        margin-bottom: 0px;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
# Objectif : Permettre à l'utilisateur de naviguer entre les différentes sections du tableau de bord
with st.sidebar:
    st.title("DASHBOARD")
    st.markdown("---")
    # Liste des options du menu
    menu = st.radio(
        "Navigation",
        ["ACCUEIL", "DONNÉES", "RESUME", "IMPUTATION", "ANALYSES", "VISUALISATION", "CORRÉLATIONS", "RÉGRESSION LINÉAIRE", "TESTS STATISTIQUES"],
        key="navigation_menu"
    )

# Main title
st.title("Tableau de Bord Statistique")

# Content based on menu selection
if menu == "ACCUEIL":
    # Welcome Banner
    st.markdown("""
    <div class="welcome-banner">
        <h2>Explorez vos Données comme Jamais !</h2>
        <p>Découvrez des insights puissants avec notre tableau de bord statistique intuitif et moderne.</p>
    </div>
    """, unsafe_allow_html=True)

    # Features Section with Cards
    st.subheader("Pourquoi choisir notre outil ?")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <i>📤</i>
            <h4>Importation Facile</h4>
            <p>Téléchargez vos fichiers (CSV, Excel, JSON, TXT) en un clic pour commencer l'analyse.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <i>📊</i>
            <h4>Visualisations Interactives</h4>
            <p>Créez des graphiques personnalisés pour explorer vos données.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <i>📈</i>
            <h4>Tests Statistiques</h4>
            <p>Validez vos hypothèses avec des tests rigoureux.</p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <i>📝</i>
            <h4>Analyse Descriptive</h4>
            <p>Obtenez des statistiques détaillées sur vos variables.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <i>🖥️</i>
            <h4>Interface Intuitive</h4>
            <p>Naviguez facilement entre les différentes fonctionnalités.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <i>⚡</i>
            <h4>Rapide et Efficace</h4>
            <p>Analysez vos données en temps réel sans attendre.</p>
        </div>
        """, unsafe_allow_html=True)

    # Call-to-Action Button
    st.markdown('<div class="cta-button">', unsafe_allow_html=True)
    if st.button("Commencez l'Analyse Maintenant !"):
        st.info("Veuillez sélectionner l'onglet 'DONNÉES' dans la barre latérale pour importer votre fichier.")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "DONNÉES":
    st.header("Chargement des Données")
    st.markdown('<div class="info-box">Importez vos données (CSV, Excel, JSON, TXT) pour commencer l’analyse. Assurez-vous que votre fichier est bien formaté.</div>', unsafe_allow_html=True)

    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'uploaded_file_name' not in st.session_state:
        st.session_state.uploaded_file_name = None

    # File uploader in a styled section
    with st.container():
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("Importer un Fichier")
        uploaded_file = st.file_uploader(
            "Choisir un fichier (CSV, Excel, JSON, TXT)",
            type=["csv", "xlsx", "xls", "json", "txt"],
            help="Sélectionnez un fichier (max 200 Mo). Formats supportés : CSV, Excel (.xlsx, .xls), JSON, TXT."
        )

        if uploaded_file is not None:
            try:
                # Get the file extension
                file_extension = uploaded_file.name.split('.')[-1].lower()

                # Read the file based on its extension
                if file_extension == "csv":
                    data = pd.read_csv(uploaded_file)
                elif file_extension in ["xlsx", "xls"]:
                    data = pd.read_excel(uploaded_file, engine='openpyxl')
                elif file_extension == "json":
                    data = pd.read_json(uploaded_file)
                elif file_extension == "txt":
                    # For TXT, allow user to specify delimiter
                    delimiter = st.selectbox(
                        "Séparateur pour le fichier TXT",
                        options=[",", "\t", ";", " "],
                        help="Choisissez le séparateur utilisé dans votre fichier texte."
                    )
                    uploaded_file.seek(0)  # Reset file pointer to the beginning
                    data = pd.read_table(uploaded_file, sep=delimiter)
                else:
                    st.markdown('<div class="error-box">Format de fichier non supporté. Veuillez utiliser un fichier CSV, Excel, JSON ou TXT.</div>', unsafe_allow_html=True)
                    data = None

                if data is not None:
                    st.session_state.data = data
                    st.session_state.uploaded_file_name = uploaded_file.name
                    st.success(f"Fichier '{uploaded_file.name}' chargé avec succès ! 🎉")
            except Exception as e:
                st.markdown(f'<div class="error-box">Erreur lors du chargement : {str(e)}</div>', unsafe_allow_html=True)
                st.session_state.data = None
                st.session_state.uploaded_file_name = None

        st.markdown('</div>', unsafe_allow_html=True)

    # Data preview section
    if st.session_state.data is not None:
        data = st.session_state.data
        with st.container():
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.subheader("Aperçu des Données")
            if st.session_state.uploaded_file_name:
                st.write(f"Fichier chargé : **{st.session_state.uploaded_file_name}**")

            col1, col2 = st.columns([3, 1])
            with col1:
                row_options = [5, 10, 25, 50, "Toutes"]
                rows_to_show = st.selectbox("Nombre de lignes à afficher", options=row_options, index=1, help="Choisissez combien de lignes afficher.")
            with col2:
                st.write(f"Total : {len(data)} lignes, {len(data.columns)} colonnes")

            if rows_to_show == "Toutes":
                st.dataframe(data, use_container_width=True)
                st.write(f"Affichage de toutes les {len(data)} lignes")
            else:
                st.dataframe(data.head(rows_to_show), use_container_width=True)
                st.write(f"Affichage des {rows_to_show} premières lignes sur {len(data)} lignes totales")

            # Download button for the data (as CSV)
            csv_buffer = io.StringIO()
            data.to_csv(csv_buffer, index=False)
            st.download_button(
                label="Télécharger les données",
                data=csv_buffer.getvalue(),
                file_name=f"{st.session_state.uploaded_file_name.rsplit('.', 1)[0] or 'data'}.csv",
                mime="text/csv",
                help="Téléchargez les données actuellement chargées sous forme de fichier CSV."
            )
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Aucun fichier chargé. Veuillez importer un fichier pour commencer.")

elif menu == "RESUME":
    st.header("Résumé des Données")
    st.markdown('<div class="info-box">Obtenez un aperçu statistique complet de vos données.</div>', unsafe_allow_html=True)

    if 'data' in st.session_state and st.session_state.data is not None:
        data = st.session_state.data

        # Summary table in a styled section
        with st.container():
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.subheader("Statistiques Descriptives")
            stats_list = []
            for col in data.columns:
                col_stats = {}
                col_stats['Colonne'] = col
                col_stats['Classe'] = 'Numérique' if pd.api.types.is_numeric_dtype(data[col]) else 'Character'
                col_stats['Éléments uniques'] = data[col].nunique()

                if pd.api.types.is_numeric_dtype(data[col]):
                    col_stats['Max'] = data[col].max()
                    col_stats['Min'] = data[col].min()
                    col_stats['Moyenne'] = data[col].mean()
                    col_stats['Médiane'] = data[col].median()
                    col_stats['Écart-type'] = data[col].std()
                    col_stats['Variance'] = data[col].var()
                else:
                    col_stats['Max'] = '-'
                    col_stats['Min'] = '-'
                    col_stats['Moyenne'] = '-'
                    col_stats['Médiane'] = '-'
                    col_stats['Écart-type'] = '-'
                    col_stats['Variance'] = '-'

                col_stats['Valeurs manquantes'] = data[col].isnull().sum()
                stats_list.append(col_stats)

            summary_df = pd.DataFrame(stats_list)

            def format_value(val):
                if isinstance(val, (int, float)) and not pd.isna(val):
                    return f"{val:.2f}"
                return val

            formatted_df = summary_df.copy()
            for col in ['Max', 'Min', 'Moyenne', 'Médiane', 'Écart-type', 'Variance']:
                formatted_df[col] = formatted_df[col].apply(format_value)

            st.dataframe(formatted_df, use_container_width=True)

            # Download summary as CSV
            csv_buffer = io.StringIO()
            formatted_df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="Télécharger le résumé",
                data=csv_buffer.getvalue(),
                file_name="summary_statistics.csv",
                mime="text/csv",
                help="Téléchargez les statistiques descriptives sous forme de fichier CSV."
            )
            st.markdown('</div>', unsafe_allow_html=True)

        # Additional analyses in an expander
        with st.expander("Analyses Rapides"):
            st.write(f"**Nombre total de colonnes** : {len(data.columns)}")
            st.write(f"**Nombre total de lignes** : {len(data)}")
            missing_cols = formatted_df[formatted_df['Valeurs manquantes'] > 0]['Colonne'].tolist()
            if missing_cols:
                st.warning(f"Colonnes avec valeurs manquantes : {', '.join(missing_cols)}")
            else:
                st.success("Aucune valeur manquante détectée dans le jeu de données.")
    else:
        st.markdown('<div class="error-box">Veuillez d\'abord charger des données dans l\'onglet DONNÉES.</div>', unsafe_allow_html=True)

elif menu == "IMPUTATION":
    st.header("Imputation des Valeurs Manquantes")
    st.markdown('<div class="info-box">Corrigez les valeurs manquantes dans vos données pour une analyse plus précise.</div>', unsafe_allow_html=True)

    if 'data' in st.session_state and st.session_state.data is not None:
        data = st.session_state.data

        # Missing values overview
        with st.container():
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.subheader("Aperçu des Valeurs Manquantes")
            missing_data = data.isnull().sum()
            missing_df = pd.DataFrame({
                "Colonne": data.columns,
                "Valeurs Manquantes": missing_data,
                "Pourcentage (%)": (missing_data / len(data) * 100).round(2)
            })
            st.dataframe(missing_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Imputation section
        if data.isnull().values.any():
            with st.container():
                st.markdown('<div class="section-box">', unsafe_allow_html=True)
                st.subheader("Imputation")
                st.markdown('<div class="missing-values-warning">DES VALEURS MANQUANTES ONT ÉTÉ TROUVÉES</div>', unsafe_allow_html=True)

                column_to_impute = st.selectbox("Colonne à imputer", options=data.columns.tolist(), help="Sélectionnez une colonne contenant des valeurs manquantes.")

                if data[column_to_impute].isnull().sum() > 0:
                    is_numeric = pd.api.types.is_numeric_dtype(data[column_to_impute])
                    st.write("Méthode d'imputation :")
                    if is_numeric:
                        imputation_method = st.selectbox(
                            "Méthode",
                            options=["Moyenne", "Écart-type", "Min", "Max", "Remplacer par 0", "Supprimer la colonne"],
                            help="Choisissez une méthode pour imputer les valeurs manquantes."
                        )
                    else:
                        imputation_method = st.selectbox(
                            "Méthode",
                            options=["Mode", "Supprimer la colonne"],
                            help="Choisissez une méthode pour imputer les valeurs manquantes."
                        )

                    if st.button("Appliquer l'imputation"):
                        data_copy = data.copy()
                        if is_numeric:
                            if imputation_method == "Moyenne":
                                mean_value = data_copy[column_to_impute].mean()
                                data_copy[column_to_impute].fillna(mean_value, inplace=True)
                                st.success(f"Les valeurs manquantes dans '{column_to_impute}' ont été remplacées par la moyenne ({mean_value:.2f}).")
                            elif imputation_method == "Écart-type":
                                std_value = data_copy[column_to_impute].std()
                                data_copy[column_to_impute].fillna(std_value, inplace=True)
                                st.success(f"Les valeurs manquantes dans '{column_to_impute}' ont été remplacées par l'écart-type ({std_value:.2f}).")
                            elif imputation_method == "Min":
                                min_value = data_copy[column_to_impute].min()
                                data_copy[column_to_impute].fillna(min_value, inplace=True)
                                st.success(f"Les valeurs manquantes dans '{column_to_impute}' ont été remplacées par le minimum ({min_value}).")
                            elif imputation_method == "Max":
                                max_value = data_copy[column_to_impute].max()
                                data_copy[column_to_impute].fillna(max_value, inplace=True)
                                st.success(f"Les valeurs manquantes dans '{column_to_impute}' ont été remplacées par le maximum ({max_value}).")
                            elif imputation_method == "Remplacer par 0":
                                data_copy[column_to_impute].fillna(0, inplace=True)
                                st.success(f"Les valeurs manquantes dans '{column_to_impute}' ont été remplacées par 0.")
                            elif imputation_method == "Supprimer la colonne":
                                data_copy = data_copy.drop(columns=[column_to_impute])
                                st.success(f"La colonne '{column_to_impute}' a été supprimée.")
                        else:
                            if imputation_method == "Mode":
                                mode_value = data_copy[column_to_impute].mode()[0]
                                data_copy[column_to_impute].fillna(mode_value, inplace=True)
                                st.success(f"Les valeurs manquantes dans '{column_to_impute}' ont été remplacées par le mode ({mode_value}).")
                            elif imputation_method == "Supprimer la colonne":
                                data_copy = data_copy.drop(columns=[column_to_impute])
                                st.success(f"La colonne '{column_to_impute}' a été supprimée.")

                        st.session_state.data = data_copy
                        st.info("Données mises à jour. Consultez l'onglet 'DONNÉES' pour voir les modifications.")
                else:
                    st.info(f"Aucune valeur manquante trouvée dans la colonne '{column_to_impute}'.")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("Aucune valeur manquante trouvée dans le jeu de données. ✅")
    else:
        st.markdown('<div class="error-box">Veuillez d\'abord charger des données dans l\'onglet DONNÉES.</div>', unsafe_allow_html=True)

elif menu == "VISUALISATION":
    st.header("Visualisation des Données")
    st.markdown('<div class="info-box">Explorez vos données avec des visualisations interactives et des statistiques.</div>', unsafe_allow_html=True)

    if 'data' in st.session_state and st.session_state.data is not None:
        data = st.session_state.data

        with st.container():
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.subheader("Sélection des Variables")
            # Multiselect for columns
            selected_columns = st.multiselect(
                "Colonnes à visualiser",
                data.columns.tolist(),
                help="Sélectionnez une ou plusieurs colonnes pour générer des visualisations. Pour 'Nuage de points', sélectionnez exactement deux colonnes numériques."
            )

            if selected_columns:
                # Separate numeric and non-numeric columns
                numeric_selected_columns = [col for col in selected_columns if pd.api.types.is_numeric_dtype(data[col])]
                non_numeric_selected_columns = [col for col in selected_columns if not pd.api.types.is_numeric_dtype(data[col])]

                # Handle numeric columns
                if numeric_selected_columns:
                    with st.expander("Visualisations pour les colonnes numériques", expanded=True):
                        # Check if there are enough numeric columns for scatter plot
                        if len(numeric_selected_columns) < 2:
                            st.warning("L'option 'Nuage de points' nécessite la sélection d'exactement **deux colonnes numériques**. Veuillez sélectionner une autre colonne numérique pour activer cette visualisation.")
                        elif len(numeric_selected_columns) > 2:
                            st.warning("L'option 'Nuage de points' nécessite exactement **deux colonnes numériques**. Veuillez sélectionner exactement deux colonnes numériques pour activer cette visualisation.")
                        
                        # Define visualization options
                        viz_options = ["Densité", "Histogramme", "Diagramme en boîte"]
                        if statsmodels_available:
                            viz_options.append("Q-Q Plot")
                        if len(numeric_selected_columns) == 2:  # Changed condition to exactly 2 columns
                            viz_options.append("Nuage de points")
                        viz_type = st.radio(
                            "Type de visualisation",
                            viz_options,
                            key="numeric_viz_type",
                            help="Sélectionnez un type de visualisation. 'Nuage de points' nécessite exactement deux colonnes numériques."
                        )

                        if viz_type == "Nuage de points" and len(numeric_selected_columns) == 2:
                            # Get the two selected numeric columns
                            x_col, y_col = numeric_selected_columns

                            # Customization options for scatter plot
                            st.subheader("Options de Personnalisation")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                point_size = st.slider(
                                    "Taille des points",
                                    min_value=10,
                                    max_value=200,
                                    value=50,
                                    step=10,
                                    key="scatter_point_size",
                                    help="Ajustez la taille des points dans le nuage de points."
                                )
                            with col2:
                                point_alpha = st.slider(
                                    "Transparence (Alpha)",
                                    min_value=0.1,
                                    max_value=1.0,
                                    value=0.6,
                                    step=0.1,
                                    key="scatter_alpha",
                                    help="Ajustez la transparence des points pour mieux voir les superpositions."
                                )
                            with col3:
                                show_regression = st.checkbox(
                                    "Afficher la ligne de régression",
                                    value=False,
                                    key="show_regression_numeric",
                                    help="Ajoute une ligne de régression pour visualiser la tendance linéaire."
                                )

                            # Create the scatter plot
                            fig, ax = plt.subplots(figsize=(10, 6))
                            sns.scatterplot(
                                data=data,
                                x=x_col,
                                y=y_col,
                                size=point_size,
                                alpha=point_alpha,
                                ax=ax,
                                color='#007bff'
                            )

                            if show_regression:
                                # Add regression line
                                sns.regplot(
                                    data=data,
                                    x=x_col,
                                    y=y_col,
                                    scatter=False,
                                    color='red',
                                    ax=ax
                                )

                            # Customize the plot
                            ax.set_title(f"Nuage de Points : {y_col} vs {x_col}", fontsize=14, pad=15)
                            ax.set_xlabel(x_col, fontsize=12)
                            ax.set_ylabel(y_col, fontsize=12)
                            ax.grid(True, linestyle='--', alpha=0.7)

                            # Adjust layout to prevent label cutoff
                            plt.tight_layout()

                            # Display the plot
                            st.pyplot(fig)
                            plt.close(fig)

                        else:
                            for col in numeric_selected_columns:
                                st.markdown(f"### Visualisation pour : {col}")
                                if viz_type == "Densité":
                                    fig, ax = plt.subplots(figsize=(10, 6))
                                    sns.kdeplot(data=data[col], fill=True, ax=ax, color='#007bff')
                                    ax.set_title(f"Densité de {col}", fontsize=14, pad=15)
                                    ax.set_xlabel(col)
                                    ax.set_ylabel("Densité")
                                    st.pyplot(fig)
                                    plt.close(fig)

                                elif viz_type == "Histogramme":
                                    num_bins = st.slider(
                                        "Nombre de barres",
                                        min_value=1,
                                        max_value=50,
                                        value=30,
                                        step=1,
                                        key=f"bins_{col}",
                                        help="Ajustez le nombre de barres pour l'histogramme."
                                    )
                                    fig, ax = plt.subplots(figsize=(10, 6))
                                    sns.histplot(data=data[col], bins=num_bins, ax=ax, color='#007bff')
                                    ax.set_title(f"Histogramme de {col}", fontsize=14, pad=15)
                                    ax.set_xlabel(col)
                                    ax.set_ylabel("Nombre")
                                    st.pyplot(fig)
                                    plt.close(fig)

                                elif viz_type == "Diagramme en boîte":
                                    box_width = st.slider(
                                        "Largeur des boîtes",
                                        min_value=0.1,
                                        max_value=1.0,
                                        value=0.5,
                                        step=0.1,
                                        key=f"box_width_{col}",
                                        help="Ajustez la largeur des boîtes."
                                    )
                                    fig, ax = plt.subplots(figsize=(10, 6))
                                    sns.boxplot(y=data[col], ax=ax, width=box_width, color='#007bff')
                                    ax.set_title(f"Diagramme en boîte de {col}", fontsize=14, pad=15)

                                    q1 = data[col].quantile(0.25)
                                    q3 = data[col].quantile(0.75)
                                    median = data[col].median()
                                    min_val = data[col].min()
                                    max_val = data[col].max()

                                    ax.text(1.1, q1, f"Q1: {q1:.1f}", verticalalignment='center', fontsize=10, color='black')
                                    ax.text(1.1, q3, f"Q3: {q3:.1f}", verticalalignment='center', fontsize=10, color='black')
                                    ax.text(1.1, median, f"Médiane: {median:.1f}", verticalalignment='center', fontsize=10, color='black')
                                    ax.text(1.1, min_val, f"Min: {min_val:.1f}", verticalalignment='center', fontsize=10, color='black')
                                    ax.text(1.1, max_val, f"Max: {max_val:.1f}", verticalalignment='center', fontsize=10, color='black')

                                    plt.subplots_adjust(right=0.75)
                                    st.pyplot(fig)
                                    plt.close(fig)

                                elif viz_type == "Q-Q Plot" and statsmodels_available:
                                    fig, ax = plt.subplots(figsize=(10, 6))
                                    sm.qqplot(data[col].dropna(), line='45', ax=ax)
                                    ax.set_title(f"Q-Q Plot de {col}", fontsize=14, pad=15)
                                    st.pyplot(fig)
                                    plt.close(fig)

                # Handle non-numeric columns
                if non_numeric_selected_columns:
                    with st.expander("Visualisations pour les colonnes non numériques", expanded=True):
                        viz_options = ["Diagramme de comptage", "Diagramme circulaire"]
                        viz_type = st.radio(
                            "Type de visualisation",
                            viz_options,
                            key="non_numeric_viz_type"
                        )

                        for col in non_numeric_selected_columns:
                            st.markdown(f"### Visualisation pour : {col}")
                            if viz_type == "Diagramme de comptage":
                                if data[col].nunique() <= 20:
                                    fig, ax = plt.subplots(figsize=(10, 6))
                                    sns.countplot(y=data[col], order=data[col].value_counts().index, ax=ax, palette='Blues')
                                    plt.title(f"Distribution de {col}", fontsize=14, pad=15)
                                    st.pyplot(fig)
                                    plt.close(fig)
                                else:
                                    st.warning(f"La colonne {col} a trop de valeurs uniques ({data[col].nunique()}) pour une visualisation claire.")

                            elif viz_type == "Diagramme circulaire":
                                if data[col].nunique() <= 20:
                                    value_counts = data[col].value_counts()
                                    labels = value_counts.index
                                    sizes = value_counts.values
                                    fig, ax = plt.subplots(figsize=(8, 8))
                                    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10}, colors=sns.color_palette('Blues', len(labels)))
                                    ax.set_title(f"Répartition de {col}", fontsize=14, pad=15)
                                    ax.axis('equal')
                                    st.pyplot(fig)
                                    plt.close(fig)
                                else:
                                    st.warning(f"La colonne {col} a trop de valeurs uniques ({data[col].nunique()}) pour une visualisation claire.")

            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="error-box">Veuillez d\'abord charger des données dans l\'onglet DONNÉES.</div>', unsafe_allow_html=True)
elif menu == "ANALYSES":
    # Section : Générateur d'Analyses
    # Objectif : Fournir des analyses automatiques des données (valeurs aberrantes, tendances, relations)
    st.header("Générateur d'Analyses")
    st.markdown('<div class="info-box">Obtenez des analyses automatiques sur vos données pour guider votre exploration.</div>', unsafe_allow_html=True)

    # Vérifier si des données sont chargées dans la session
    if 'data' in st.session_state and st.session_state.data is not None:
        data = st.session_state.data
        # Liste pour stocker les analyses textuelles à exporter
        insights_text = []

        # Partie 1 : Détection des Valeurs Aberrantes
        # Objectif : Identifier les outliers dans les colonnes numériques avec la méthode IQR
        with st.expander("Détection des Valeurs Aberrantes", expanded=True):
            st.subheader("Valeurs Aberrantes")
            # Sélectionner les colonnes numériques
            numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
            if not numeric_columns:
                # Afficher un avertissement si aucune colonne numérique n'est disponible
                st.warning("Aucune colonne numérique trouvée pour la détection des valeurs aberrantes.")
            else:
                # Liste pour stocker les analyses sur les outliers
                outlier_insights = []
                for col in numeric_columns:
                    # Calculer les quartiles et l'IQR pour détecter les outliers
                    Q1 = data[col].quantile(0.25)
                    Q3 = data[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    # Identifier les valeurs aberrantes
                    outliers = data[(data[col] < lower_bound) | (data[col] > upper_bound)][col]
                    if not outliers.empty:
                        # Ajouter l'analyse à la liste
                        outlier_insights.append(f"- **{col}** : {len(outliers)} valeurs aberrantes détectées (inférieur à {lower_bound:.2f} ou supérieur à {upper_bound:.2f})")
                        # Visualisation : Diagramme en boîte pour montrer les outliers
                        fig, ax = plt.subplots(figsize=(10, 6))
                        sns.boxplot(x=data[col], ax=ax, color='#007bff')
                        ax.set_title(f"Diagramme en boîte pour {col} (Valeurs Aberrantes)", fontsize=14, pad=15)
                        ax.set_xlabel(col)
                        st.pyplot(fig)
                        plt.close(fig)
                if outlier_insights:
                    # Ajouter les analyses au rapport textuel et les afficher
                    insights_text.append("### Valeurs Aberrantes\n" + "\n".join(outlier_insights))
                    for insight in outlier_insights:
                        st.markdown(insight)
                else:
                    # Message de confirmation si aucune valeur aberrante n'est trouvée
                    st.success("Aucune valeur aberrante détectée dans les colonnes numériques.")

        # Partie 2 : Analyse des Tendances
        # Objectif : Détecter les tendances croissantes ou décroissantes dans les données
        with st.expander("Analyse des Tendances", expanded=True):
            st.subheader("Tendances")
            # Identifier les colonnes de type datetime
            date_columns = data.select_dtypes(include=['datetime']).columns.tolist()
            # Identifier les colonnes numériques
            numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
            trend_insights = []
            if date_columns and numeric_columns:
                # Utiliser la première colonne datetime comme axe temporel
                date_col = date_columns[0]
                for num_col in numeric_columns:
                    # Trier les données par date et supprimer les valeurs manquantes
                    data_sorted = data[[date_col, num_col]].dropna().sort_values(by=date_col)
                    if len(data_sorted) > 1:
                        # Vérifier si la colonne est monotone (croissante ou décroissante)
                        increasing = data_sorted[num_col].is_monotonic_increasing
                        decreasing = data_sorted[num_col].is_monotonic_decreasing
                        if increasing:
                            trend_insights.append(f"- **{num_col}** montre une tendance croissante par rapport à {date_col}.")
                        elif decreasing:
                            trend_insights.append(f"- **{num_col}** montre une tendance décroissante par rapport à {date_col}.")
                        if increasing or decreasing:
                            # Visualisation : Graphique linéaire pour montrer la tendance
                            fig, ax = plt.subplots(figsize=(10, 6))
                            sns.lineplot(x=date_col, y=num_col, data=data_sorted, ax=ax, color='#007bff')
                            ax.set_title(f"Tendance de {num_col} par rapport à {date_col}", fontsize=14, pad=15)
                            ax.set_xlabel(date_col)
                            ax.set_ylabel(num_col)
                            plt.xticks(rotation=45)
                            plt.tight_layout()
                            st.pyplot(fig)
                            plt.close(fig)
            else:
                # Si aucune colonne datetime, analyser les tendances par index
                for num_col in numeric_columns:
                    data_series = data[num_col].dropna()
                    if len(data_series) > 1:
                        # Vérifier si la série est monotone
                        increasing = data_series.is_monotonic_increasing
                        decreasing = data_series.is_monotonic_decreasing
                        if increasing:
                            trend_insights.append(f"- **{num_col}** montre une tendance croissante sur les lignes.")
                        elif decreasing:
                            trend_insights.append(f"- **{num_col}** montre une tendance décroissante sur les lignes.")
                        if increasing or decreasing:
                            # Visualisation : Graphique linéaire par index
                            fig, ax = plt.subplots(figsize=(10, 6))
                            sns.lineplot(x=data_series.index, y=data_series, ax=ax, color='#007bff')
                            ax.set_title(f"Tendance de {num_col} sur les lignes", fontsize=14, pad=15)
                            ax.set_xlabel("Index")
                            ax.set_ylabel(num_col)
                            plt.tight_layout()
                            st.pyplot(fig)
                            plt.close(fig)
            if trend_insights:
                # Ajouter les analyses au rapport textuel et les afficher
                insights_text.append("### Tendances\n" + "\n".join(trend_insights))
                for insight in trend_insights:
                    st.markdown(insight)
            else:
                # Message si aucune tendance n'est détectée
                st.info("Aucune tendance claire détectée dans les données.")

        # Partie 3 : Suggestions de Relations
        # Objectif : Identifier les corrélations significatives entre variables numériques
        with st.expander("Suggestions de Relations", expanded=True):
            st.subheader("Relations Potentielles")
            # Sélectionner les colonnes numériques
            numeric_data = data.select_dtypes(include=[np.number])
            if len(numeric_data.columns) < 2:
                # Avertissement si moins de deux colonnes numériques
                st.warning("Au moins deux colonnes numériques sont nécessaires pour analyser les relations.")
            else:
                # Calculer la matrice de corrélation
                corr_matrix = numeric_data.corr()
                # Identifier les corrélations fortes (|r| > 0.5, hors diagonale)
                strong_corrs = corr_matrix[(corr_matrix.abs() > 0.5) & (corr_matrix != 1.0)].stack().reset_index()
                relationship_insights = []
                if not strong_corrs.empty:
                    strong_corrs.columns = ['Variable 1', 'Variable 2', 'Corrélation']
                    for _, row in strong_corrs.iterrows():
                        var1, var2, corr = row['Variable 1'], row['Variable 2'], row['Corrélation']
                        # Ajouter l'analyse à la liste
                        relationship_insights.append(f"- **{var1}** et **{var2}** ont une corrélation de {corr:.2f}, suggérant une relation potentielle.")
                        # Visualisation : Nuage de points pour la paire
                        fig, ax = plt.subplots(figsize=(10, 6))
                        sns.scatterplot(x=data[var1], y=data[var2], ax=ax, color='#007bff')
                        ax.set_title(f"Relation entre {var1} et {var2} (Corrélation = {corr:.2f})", fontsize=14, pad=15)
                        ax.set_xlabel(var1)
                        ax.set_ylabel(var2)
                        st.pyplot(fig)
                        plt.close(fig)
                if relationship_insights:
                    # Ajouter les analyses au rapport textuel et les afficher
                    insights_text.append("### Relations Potentielles\n" + "\n".join(relationship_insights))
                    for insight in relationship_insights:
                        st.markdown(insight)
                else:
                    # Message si aucune corrélation significative
                    st.info("Aucune relation significative (corrélation > 0.5) détectée entre les variables numériques.")

        # Exportation des Analyses
        # Objectif : Permettre le téléchargement d'un rapport textuel des analyses
        if insights_text:
            # Combiner toutes les analyses en un seul texte
            insights_report = "\n\n".join(insights_text)
            # Bouton de téléchargement
            st.download_button(
                label="Télécharger le Rapport d'Analyses",
                data=insights_report,
                file_name="data_analyses.txt",
                mime="text/plain",
                help="Téléchargez un rapport textuel des analyses générées."
            )
    else:
        # Afficher une erreur si aucune donnée n'est chargée
        st.markdown('<div class="error-box">Veuillez d\'abord charger des données dans l\'onglet DONNÉES.</div>', unsafe_allow_html=True)


elif menu == "CORRÉLATIONS":
    st.header("Corrélations entre les Variables")
    st.markdown('<div class="info-box">Analysez les relations entre vos variables numériques avec des visualisations de corrélations.</div>', unsafe_allow_html=True)

    if 'data' in st.session_state and st.session_state.data is not None:
        data = st.session_state.data
        numeric_data = data.select_dtypes(include=[np.number])

        if numeric_data.empty or len(numeric_data.columns) < 2:
            st.markdown('<div class="error-box">Au moins deux variables numériques sont requises pour les corrélations.</div>', unsafe_allow_html=True)
        else:
            with st.container():
                st.markdown('<div class="section-box">', unsafe_allow_html=True)
                st.subheader("Matrice de Corrélation")
                corr_matrix = numeric_data.corr()
                if corr_matrix.isnull().values.any():
                    st.warning("Valeurs manquantes détectées. Imputez les données dans l'onglet IMPUTATION pour des résultats précis.")

                colorbar_ticks = [-1.00, -0.75, -0.50, -0.25, 0.00, 0.25, 0.50, 0.75, 1.00]

                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(
                    corr_matrix,
                    annot=True,
                    fmt=".2f",
                    cmap='coolwarm',
                    vmin=-1,
                    vmax=1,
                    center=0,
                    cbar_kws={'ticks': colorbar_ticks},
                    ax=ax,
                    annot_kws={'size': 10}
                )
                ax.set_title("Matrice de Corrélation (Valeurs)", fontsize=14, pad=15)
                st.pyplot(fig)
                plt.close(fig)

                # Download correlation matrix
                csv_buffer = io.StringIO()
                corr_matrix.to_csv(csv_buffer)
                st.download_button(
                    label="Télécharger la matrice",
                    data=csv_buffer.getvalue(),
                    file_name="correlation_matrix.csv",
                    mime="text/csv",
                    help="Téléchargez la matrice de corrélation sous forme de fichier CSV."
                )
                st.markdown('</div>', unsafe_allow_html=True)

            # Correlation analyses in an expander
            with st.expander("Analyses sur les Corrélations"):
                strong_corrs = corr_matrix[(corr_matrix.abs() > 0.7) & (corr_matrix != 1.0)].stack().reset_index()
                if not strong_corrs.empty:
                    strong_corrs.columns = ['Variable 1', 'Variable 2', 'Corrélation']
                    st.write("**Corrélations fortes (|r| > 0.7) :**")
                    st.dataframe(strong_corrs, use_container_width=True)
                else:
                    st.success("Aucune corrélation forte (|r| > 0.7) détectée.")
    else:
        st.markdown('<div class="error-box">Veuillez d\'abord charger des données dans l\'onglet DONNÉES.</div>', unsafe_allow_html=True)

elif menu == "RÉGRESSION LINÉAIRE":
    st.header("Régression Linéaire")
    st.markdown('<div class="info-box">Effectuez une régression linéaire pour explorer les relations entre deux variables numériques.</div>', unsafe_allow_html=True)

    if not statsmodels_available:
        st.markdown('<div class="error-box">Le module \'statsmodels\' est requis. Installez-le avec : <code>pip install statsmodels</code>.</div>', unsafe_allow_html=True)
    else:
        if 'data' in st.session_state and st.session_state.data is not None:
            data = st.session_state.data
            numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()

            if len(numeric_columns) < 2:
                st.markdown('<div class="error-box">Au moins deux variables numériques sont requises.</div>', unsafe_allow_html=True)
            else:
                with st.container():
                    st.markdown('<div class="section-box">', unsafe_allow_html=True)
                    st.subheader("Sélection des Variables")
                    col1, col2 = st.columns(2)
                    with col1:
                        var_x = st.selectbox(
                            "Variable explicative (X)",
                            numeric_columns,
                            help="Choisissez la variable indépendante."
                        )
                    with col2:
                        var_y = st.selectbox(
                            "Variable réponse (Y)",
                            numeric_columns,
                            index=1 if len(numeric_columns) > 1 else 0,
                            help="Choisissez la variable dépendante."
                        )

                    if var_x and var_y:
                        if data[var_x].isnull().any() or data[var_y].isnull().any():
                            st.warning("Valeurs manquantes détectées dans les variables sélectionnées.")
                            if st.button("Supprimer les lignes avec valeurs manquantes", help="Supprimez les lignes contenant des valeurs manquantes pour ces variables."):
                                data_clean = data[[var_x, var_y]].dropna()
                                st.session_state.data_clean = data_clean
                                st.success("Lignes avec valeurs manquantes supprimées.")
                        else:
                            data_clean = data[[var_x, var_y]]
                            st.session_state.data_clean = data_clean

                        if st.button("Exécuter la régression", help="Lancez l'analyse de régression linéaire."):
                            with st.container():
                                st.markdown('<div class="section-box">', unsafe_allow_html=True)
                                st.subheader("Résultats de la Régression")

                                try:
                                    # Fit the regression model
                                    formula = f"{var_y} ~ {var_x}"
                                    model = smf.ols(formula=formula, data=data_clean).fit()

                                    # Extract regression statistics
                                    summary_data = {
                                        "Variable dépendante": model.model.endog_names,
                                        "Méthode": "Moindres carrés ordinaires",
                                        "R-carré": f"{model.rsquared:.3f}",
                                        "R-carré ajusté": f"{model.rsquared_adj:.3f}",
                                        "F-statistique": f"{model.fvalue:.3f}",
                                        "Prob (F-statistique)": f"{model.f_pvalue:.3f}",
                                        "Log-vraisemblance": f"{model.llf:.3f}",
                                        "Nombre d'observations": model.nobs,
                                        "AIC": f"{model.aic:.3f}",
                                        "BIC": f"{model.bic:.3f}",
                                        "Type de covariance": "non robuste"
                                    }

                                    # Display general statistics in a table
                                    st.write("**Résumé Général :**")
                                    summary_df = pd.DataFrame.from_dict(summary_data, orient='index', columns=['Valeur'])
                                    st.table(summary_df)

                                    # Extract coefficients table
                                    coef_data = {
                                        "Variable": model.params.index,
                                        "Coefficient": model.params.values,
                                        "Erreur standard": model.bse.values,
                                        "t": model.tvalues.values,
                                        "P>|t|": model.pvalues.values,
                                        "Intervalle de confiance [0.025]": model.conf_int()[0].values,
                                        "Intervalle de confiance [0.975]": model.conf_int()[1].values
                                    }
                                    coef_df = pd.DataFrame(coef_data)
                                    coef_df = coef_df.round(3)

                                    # Display coefficients table
                                    st.write("**Coefficients :**")
                                    st.dataframe(coef_df, use_container_width=True)

                                    # Compute additional statistics manually
                                    additional_stats = {}
                                    try:
                                        # Durbin-Watson
                                        from statsmodels.stats.stattools import durbin_watson
                                        dw_stat = durbin_watson(model.resid)
                                        additional_stats["Durbin-Watson"] = f"{dw_stat:.3f}"

                                        # Jarque-Bera test
                                        from statsmodels.stats.stattools import jarque_bera
                                        jb_stat, jb_pvalue = jarque_bera(model.resid)[:2]
                                        additional_stats["Jarque-Bera (JB)"] = f"{jb_stat:.3f}"
                                        additional_stats["Prob(JB)"] = f"{jb_pvalue:.3f}"

                                        # Omnibus test
                                        from statsmodels.stats.stattools import omni_normtest
                                        omni_stat, omni_pvalue = omni_normtest(model.resid)
                                        additional_stats["Omnibus"] = f"{omni_stat:.3f}"
                                        additional_stats["Prob(Omnibus)"] = f"{omni_pvalue:.3f}"

                                        # Skewness and Kurtosis using scipy.stats
                                        from scipy.stats import skew, kurtosis
                                        additional_stats["Asymétrie"] = f"{skew(model.resid):.3f}"
                                        additional_stats["Kurtosis"] = f"{kurtosis(model.resid, fisher=False):.3f}"

                                        # Condition number
                                        additional_stats["Numéro de condition"] = f"{model.condition_number:.2e}"
                                    except Exception as diag_err:
                                        st.warning(f"Impossible de calculer certaines statistiques supplémentaires : {str(diag_err)}")
                                        additional_stats["Message"] = "Certaines statistiques ne sont pas disponibles."

                                    # Display additional statistics
                                    st.write("**Statistiques supplémentaires :**")
                                    additional_df = pd.DataFrame.from_dict(additional_stats, orient='index', columns=['Valeur'])
                                    st.table(additional_df)

                                    # Notes
                                    st.write("**Notes :**")
                                    st.write("[1] Les erreurs standard supposent que la matrice de covariance des erreurs est correctement spécifiée.")
                                    st.write("[2] Le numéro de condition est élevé, ce qui peut indiquer une forte multicolinéarité ou d'autres problèmes numériques.")

                                    # Regression plot
                                    st.subheader(f"Graphique : {var_y} vs {var_x}")
                                    fig, ax = plt.subplots(figsize=(10, 6))
                                    sns.regplot(x=var_x, y=var_y, data=data_clean, ax=ax, ci=95, line_kws={"color": "red"})
                                    ax.set_xlabel(var_x)
                                    ax.set_ylabel(var_y)
                                    ax.set_title(f"Régression Linéaire : {var_y} vs {var_x}", fontsize=14, pad=15)
                                    st.pyplot(fig)
                                    plt.close(fig)

                                    # Download regression summary (in French)
                                    summary_text = (
                                        "Résumé de la Régression Linéaire\n\n"
                                        "Résumé Général\n" + summary_df.to_string() + "\n\n"
                                        "Coefficients\n" + coef_df.to_string() + "\n\n"
                                        "Statistiques supplémentaires\n" + additional_df.to_string() + "\n\n"
                                        "Notes :\n"
                                        "[1] Les erreurs standard supposent que la matrice de covariance des erreurs est correctement spécifiée.\n"
                                        "[2] Le numéro de condition est élevé, ce qui peut indiquer une forte multicolinéarité ou d'autres problèmes numériques."
                                    )
                                    st.download_button(
                                        label="Télécharger le résumé",
                                        data=summary_text,
                                        file_name="regression_summary.txt",
                                        mime="text/plain",
                                        help="Téléchargez le résumé de la régression sous forme de fichier texte."
                                    )
                                except Exception as e:
                                    st.markdown(f'<div class="error-box">Erreur : {str(e)}</div>', unsafe_allow_html=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # Data preview in an expander
                with st.expander("Aperçu des Données Sélectionnées"):
                    if 'data_clean' in st.session_state:
                        st.dataframe(st.session_state.data_clean, use_container_width=True)
                    else:
                        st.info("Exécutez la régression pour voir les données utilisées.")
        else:
            st.markdown('<div class="error-box">Veuillez d\'abord charger des données dans l\'onglet DONNÉES.</div>', unsafe_allow_html=True)

elif menu == "TESTS STATISTIQUES":
    st.header("Tests Statistiques")
    st.markdown('<div class="info-box">Validez vos hypothèses avec une variété de tests statistiques.</div>', unsafe_allow_html=True)

    if 'data' in st.session_state and st.session_state.data is not None:
        data = st.session_state.data

        # Initialize a list to store test results
        if 'test_results' not in st.session_state:
            st.session_state.test_results = []

        with st.container():
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.subheader("Sélection du Test")
            test_type = st.selectbox(
                "Type de test",
                ["Hypothèse", "Normalité (Shapiro-Wilk)", "Homoscédasticité (Levene)", "ANOVA", "T-test", "Chi-squared"],
                key="test_type_select",
                help="Choisissez le test statistique à effectuer."
            )

            if test_type == "Hypothèse":
                st.write("Choisir une variable pour le test d'hypothèse :")
                var = st.selectbox("Variable", data.columns.tolist(), key="hypothesis_var")
                hypothesis = st.text_input("Entrez votre hypothèse", key="hypothesis_input", help="Exemple : 'La moyenne est égale à 0'.")
                if st.button("EXÉCUTER LE TEST", key="run_hypothesis"):
                    if hypothesis:
                        st.info(f"Hypothèse enregistrée : {hypothesis}")
                        st.write(f"Variable sélectionnée : {var}")
                        st.warning("Ce champ est un placeholder. Aucun test statistique n'est effectué ici.")
                    else:
                        st.markdown('<div class="error-box">Veuillez entrer une hypothèse.</div>', unsafe_allow_html=True)

            elif test_type == "Normalité (Shapiro-Wilk)":
                numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
                if not numeric_columns:
                    st.markdown('<div class="error-box">Aucune variable numérique disponible.</div>', unsafe_allow_html=True)
                else:
                    var = st.selectbox(
                        "Variable",
                        numeric_columns,
                        key="shapiro_var",
                        help="Sélectionnez une variable numérique pour tester la normalité."
                    )
                    if st.button("EXÉCUTER LE TEST", key="run_shapiro"):
                        try:
                            stat, p_value = stats.shapiro(data[var].dropna())
                            result = {
                                "Test": "Normalité (Shapiro-Wilk)",
                                "Variable": var,
                                "Statistique": round(stat, 4),
                                "P-Valeur": round(p_value, 4),
                                "Interprétation": "Non normales" if p_value < 0.05 else "Normales"
                            }
                            st.session_state.test_results.append(result)
                            st.write(f"**Statistique** : {stat:.4f}, **p-valeur** : {p_value:.4f}")
                            st.write(f"**Interprétation** : {'Non normales' if p_value < 0.05 else 'Normales'} (seuil 0.05)")
                        except Exception as e:
                            st.markdown(f'<div class="error-box">Erreur : {str(e)}</div>', unsafe_allow_html=True)

            elif test_type == "Homoscédasticité (Levene)":
                numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
                categorical_columns = data.select_dtypes(exclude=[np.number]).columns.tolist()
                if not numeric_columns or not categorical_columns:
                    st.markdown('<div class="error-box">Variable numérique et catégorielle requises.</div>', unsafe_allow_html=True)
                else:
                    col1, col2 = st.columns(2)
                    with col1:
                        var_numeric = st.selectbox(
                            "Variable numérique",
                            numeric_columns,
                            key="levene_numeric",
                            help="Sélectionnez la variable numérique à tester."
                        )
                    with col2:
                        var_group = st.selectbox(
                            "Variable de groupe",
                            categorical_columns,
                            key="levene_group",
                            help="Sélectionnez la variable catégorielle pour les groupes."
                        )
                    if st.button("EXÉCUTER LE TEST", key="run_levene"):
                        try:
                            groups = [data[data[var_group] == g][var_numeric].dropna() for g in data[var_group].unique()]
                            if len(groups) < 2:
                                st.markdown('<div class="error-box">Au moins 2 catégories nécessaires.</div>', unsafe_allow_html=True)
                            else:
                                stat, p_value = stats.levene(*groups)
                                result = {
                                    "Test": "Homoscédasticité (Levene)",
                                    "Variable Numérique": var_numeric,
                                    "Groupe": var_group,
                                    "Statistique": round(stat, 4),
                                    "P-Valeur": round(p_value, 4),
                                    "Interprétation": "Variances inégales" if p_value < 0.05 else "Variances égales"
                                }
                                st.session_state.test_results.append(result)
                                st.write(f"**Statistique** : {stat:.4f}, **p-valeur** : {p_value:.4f}")
                                st.write(f"**Interprétation** : {'Variances inégales' if p_value < 0.05 else 'Variances égales'} (seuil 0.05)")
                        except Exception as e:
                            st.markdown(f'<div class="error-box">Erreur : {str(e)}</div>', unsafe_allow_html=True)

            elif test_type == "ANOVA":
                numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
                categorical_columns = data.select_dtypes(exclude=[np.number]).columns.tolist()
                if not numeric_columns or not categorical_columns:
                    st.markdown('<div class="error-box">Variable numérique et catégorielle requises.</div>', unsafe_allow_html=True)
                else:
                    col1, col2 = st.columns(2)
                    with col1:
                        var_response = st.selectbox(
                            "Variable réponse",
                            numeric_columns,
                            key="anova_response",
                            help="Sélectionnez la variable numérique dépendante."
                        )
                    with col2:
                        var_factor = st.selectbox(
                            "Variable facteur",
                            categorical_columns,
                            key="anova_factor",
                            help="Sélectionnez la variable catégorielle pour les groupes."
                        )
                    if st.button("EXÉCUTER LE TEST", key="run_anova"):
                        try:
                            groups = [data[data[var_factor] == g][var_response].dropna() for g in data[var_factor].unique()]
                            if len(groups) < 2:
                                st.markdown('<div class="error-box">Au moins 2 catégories nécessaires.</div>', unsafe_allow_html=True)
                            else:
                                stat, p_value = stats.f_oneway(*groups)
                                result = {
                                    "Test": "ANOVA",
                                    "Variable Réponse": var_response,
                                    "Facteur": var_factor,
                                    "Statistique": round(stat, 4),
                                    "P-Valeur": round(p_value, 4),
                                    "Interprétation": "Différence significative" if p_value < 0.05 else "Aucune différence"
                                }
                                st.session_state.test_results.append(result)
                                st.write(f"**Statistique F** : {stat:.4f}, **p-valeur** : {p_value:.4f}")
                                st.write(f"**Interprétation** : {'Différence significative' if p_value < 0.05 else 'Aucune différence'} (seuil 0.05)")
                        except Exception as e:
                            st.markdown(f'<div class="error-box">Erreur : {str(e)}</div>', unsafe_allow_html=True)

            elif test_type == "T-test":
                numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
                if len(numeric_columns) < 2:
                    st.markdown('<div class="error-box">Au moins deux variables numériques requises.</div>', unsafe_allow_html=True)
                else:
                    col1, col2 = st.columns(2)
                    with col1:
                        var1 = st.selectbox(
                            "Première variable",
                            numeric_columns,
                            key="ttest_var1",
                            help="Sélectionnez la première variable numérique."
                        )
                    with col2:
                        var2 = st.selectbox(
                            "Deuxième variable",
                            numeric_columns,
                            index=1 if len(numeric_columns) > 1 else 0,
                            key="ttest_var2",
                            help="Sélectionnez la deuxième variable numérique."
                        )
                    if st.button("EXÉCUTER LE TEST", key="run_ttest"):
                        try:
                            stat, p_value = stats.ttest_ind(data[var1].dropna(), data[var2].dropna(), equal_var=False)
                            result = {
                                "Test": "T-test",
                                "Variable 1": var1,
                                "Variable 2": var2,
                                "Statistique": round(stat, 4),
                                "P-Valeur": round(p_value, 4),
                                "Interprétation": "Différence significative" if p_value < 0.05 else "Aucune différence"
                            }
                            st.session_state.test_results.append(result)
                            st.write(f"**Statistique T** : {stat:.4f}, **p-valeur** : {p_value:.4f}")
                            st.write(f"**Interprétation** : {'Différence significative' if p_value < 0.05 else 'Aucune différence'} (seuil 0.05)")
                        except Exception as e:
                            st.markdown(f'<div class="error-box">Erreur : {str(e)}</div>', unsafe_allow_html=True)

            elif test_type == "Chi-squared":
                categorical_columns = data.select_dtypes(exclude=[np.number]).columns.tolist()
                if len(categorical_columns) < 2:
                    st.markdown('<div class="error-box">Au moins deux variables catégorielles requises.</div>', unsafe_allow_html=True)
                else:
                    col1, col2 = st.columns(2)
                    with col1:
                        var1 = st.selectbox(
                            "Première variable",
                            categorical_columns,
                            key="chi2_var1",
                            help="Sélectionnez la première variable catégorielle."
                        )
                    with col2:
                        var2 = st.selectbox(
                            "Deuxième variable",
                            categorical_columns,
                            index=1 if len(categorical_columns) > 1 else 0,
                            key="chi2_var2",
                            help="Sélectionnez la deuxième variable catégorielle."
                        )
                    if st.button("EXÉCUTER LE TEST", key="run_chi2"):
                        try:
                            contingency = pd.crosstab(data[var1], data[var2])
                            chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
                            result = {
                                "Test": "Chi-squared",
                                "Variable 1": var1,
                                "Variable 2": var2,
                                "Statistique": round(chi2, 4),
                                "P-Valeur": round(p_value, 4),
                                "Degré de Liberté": dof,
                                "Interprétation": "Association significative" if p_value < 0.05 else "Aucune association"
                            }
                            st.session_state.test_results.append(result)
                            st.write(f"**Statistique Chi²** : {chi2:.4f}, **p-valeur** : {p_value:.4f}")
                            st.write(f"**Degré de liberté** : {dof}")
                            st.write(f"**Interprétation** : {'Association significative' if p_value < 0.05 else 'Aucune association'} (seuil 0.05)")
                        except Exception as e:
                            st.markdown(f'<div class="error-box">Erreur : {str(e)}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Test results summary in an expander
        with st.expander("Résumé des Tests Effectués"):
            if st.session_state.test_results:
                results_df = pd.DataFrame(st.session_state.test_results)
                st.dataframe(results_df, use_container_width=True)
                csv_buffer = io.StringIO()
                results_df.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="Télécharger les résultats",
                    data=csv_buffer.getvalue(),
                    file_name="test_results.csv",
                    mime="text/csv",
                    help="Téléchargez les résultats des tests sous forme de fichier CSV."
                )
            else:
                st.info("Aucun test effectué pour le moment.")
    else:
        st.markdown('<div class="error-box">Veuillez d\'abord charger des données dans l\'onglet DONNÉES.</div>', unsafe_allow_html=True)