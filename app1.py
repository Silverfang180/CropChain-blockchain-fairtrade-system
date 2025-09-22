import streamlit as st
import datetime
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="Blockchain Fair Trade System",
    page_icon="🌿",
    layout="wide"
)

# --- Simulated Blockchain & State Management ---

# Initialize session state for the blockchain, products, and logs if they don't exist.
# This ensures data persists across user interactions.
if 'blockchain' not in st.session_state:
    st.session_state['blockchain'] = []
if 'products' not in st.session_state:
    st.session_state['products'] = {} # Using a dictionary for easy product lookup

# --- Helper Functions ---

def add_block(product_id, product_name, owner, owner_type, price, action, previous_owner="Genesis"):
    """
    Adds a new transaction (a "block") to our simulated blockchain.
    """
    block = {
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ProductID": product_id,
        "ProductName": product_name,
        "Owner": owner,
        "Price (INR)": f"{price:,.2f}",
        "Action": action,
        "PreviousOwner": previous_owner,
    }
    st.session_state.blockchain.append(block)

# --- UI Layout ---

st.title("🌿 Blockchain-Based Fair Trade System")
st.markdown("A Streamlit prototype demonstrating a transparent and equitable supply chain, as detailed in the project report.")

# --- Main Application Columns ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.header("Stakeholder Actions")

    # --- 1. Farmer Panel ---
    with st.expander("👨‍🌾 Farmer: Register New Product", expanded=True):
        with st.form("farmer_form"):
            farmer_name = st.text_input("Farmer's Name", placeholder="e.g., Ram Singh")
            product_name = st.text_input("Product Name", placeholder="e.g., Organic Coffee Beans")
            base_price = st.number_input("Base Price (INR)", min_value=0.0, format="%.2f")
            submitted = st.form_submit_button("Register Product on Blockchain")

            if submitted:
                if not farmer_name or not product_name or base_price <= 0:
                    st.error("Please fill in all fields with valid data.")
                else:
                    product_id = f"PROD-{len(st.session_state.products) + 1:04d}"
                    # Update product state
                    st.session_state.products[product_id] = {
                        "name": product_name,
                        "current_owner": farmer_name,
                        "owner_type": 'Farmer'
                    }
                    # Add to blockchain
                    add_block(product_id, product_name, farmer_name, 'Farmer', base_price, "Registered by Farmer")
                    st.success(f"Product '{product_name}' ({product_id}) registered successfully by {farmer_name}!")

    # --- 2. Distributor Panel ---
    with st.expander("🚚 Distributor: Purchase from Farmer"):
        # Get products currently owned by farmers
        farmer_products = {pid: p for pid, p in st.session_state.products.items() if p['owner_type'] == 'Farmer'}
        
        if not farmer_products:
            st.info("No products available for purchase from farmers.")
        else:
            with st.form("distributor_form"):
                product_ids = list(farmer_products.keys())
                product_display = [f"{pid} - {farmer_products[pid]['name']}" for pid in product_ids]
                
                selected_display = st.selectbox("Select Product to Purchase", options=product_display)
                distributor_price = st.number_input("New Price (INR)", min_value=0.0, format="%.2f")
                submitted = st.form_submit_button("Purchase from Farmer")

                if submitted and selected_display:
                    selected_id = selected_display.split(" - ")[0]
                    product = st.session_state.products[selected_id]
                    previous_owner = product['current_owner']
                    
                    # Update product state
                    product['current_owner'] = "Distributor"
                    product['owner_type'] = 'Distributor'
                    
                    # Add to blockchain
                    add_block(selected_id, product['name'], "Distributor", 'Distributor', distributor_price, "Purchased by Distributor", previous_owner)
                    st.success(f"Product {selected_id} purchased from {previous_owner}!")

    # --- 3. Retailer Panel ---
    with st.expander("🏪 Retailer: Purchase from Distributor"):
        # Get products currently owned by distributors
        distributor_products = {pid: p for pid, p in st.session_state.products.items() if p['owner_type'] == 'Distributor'}

        if not distributor_products:
            st.info("No products available for purchase from distributors.")
        else:
            with st.form("retailer_form"):
                product_ids = list(distributor_products.keys())
                product_display = [f"{pid} - {distributor_products[pid]['name']}" for pid in product_ids]
                
                selected_display = st.selectbox("Select Product to Purchase", options=product_display)
                retailer_price = st.number_input("Final Consumer Price (INR)", min_value=0.0, format="%.2f")
                submitted = st.form_submit_button("Purchase from Distributor")

                if submitted and selected_display:
                    selected_id = selected_display.split(" - ")[0]
                    product = st.session_state.products[selected_id]
                    
                    # Update product state
                    product['current_owner'] = "Retailer"
                    product['owner_type'] = 'Retailer'
                    
                    # Add to blockchain
                    add_block(selected_id, product['name'], "Retailer", 'Retailer', retailer_price, "Stocked by Retailer", "Distributor")
                    st.success(f"Product {selected_id} is now stocked and ready for sale!")


with col2:
    st.header("🔍 Consumer: Verify Product Authenticity")
    
    if not st.session_state.products:
        st.info("No products have been registered on the blockchain yet.")
    else:
        product_ids = list(st.session_state.products.keys())
        product_display_list = [f"{pid} - {st.session_state.products[pid]['name']}" for pid in product_ids]
        
        selected_product_display = st.selectbox(
            "Select a product to trace its journey",
            options=product_display_list,
            index=None,
            placeholder="Choose a product..."
        )

        if selected_product_display:
            selected_id = selected_product_display.split(" - ")[0]
            product_info = st.session_state.products[selected_id]
            
            st.subheader(f"Traceability Report for: {product_info['name']}")
            st.markdown(f"**Product ID:** `{selected_id}`")
            st.markdown(f"**Current Owner:** `{product_info['current_owner']}`")

            # Filter blockchain for this product's history
            history = [block for block in st.session_state.blockchain if block['ProductID'] == selected_id]
            
            if history:
                st.write("---")
                st.write("#### Product Journey from Farmer to Shelf:")
                for i, entry in enumerate(history):
                    st.info(f"""
                    **Step {i+1}: {entry['Action']}**
                    - **Owner:** {entry['Owner']}
                    - **Price:** ₹{entry['Price (INR)']}
                    - **Timestamp:** {entry['Timestamp']}
                    - **Previous Owner:** {entry['PreviousOwner']}
                    """)
            else:
                st.warning("No history found for this product.")

# --- Display Full Blockchain Ledger ---
st.header("🔗 Live Blockchain Ledger")
st.markdown("This table shows every transaction recorded on the immutable ledger in real-time.")

if not st.session_state.blockchain:
    st.warning("No transactions have been recorded yet.")
else:
    # Convert list of dicts to DataFrame for better display
    df = pd.DataFrame(st.session_state.blockchain)
    # Reorder columns for clarity
    df = df[["Timestamp", "ProductID", "ProductName", "Owner", "Price (INR)", "Action", "Previous Owner"]]
    st.dataframe(df, use_container_width=True, hide_index=True)
