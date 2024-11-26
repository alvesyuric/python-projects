import pandas as pd

# Initial data for the industry (products and their respective available stock)
industry_stock = pd.DataFrame({
    'Product': ['Sliced Bread', 'Cookies', 'Frozen Pizza', 'Instant Noodles', 'Pre-cooked Lasagna', 
                'Chicken Nuggets', 'Panettone', 'Hamburger Buns', 'Hot Dog Buns', 'Pastry Dough', 'Ready Cake'],
    'Quantity': [350, 120, 140, 110, 55, 150, 300, 150, 33, 350, 140],
})

# Initial data for the DC (current stock and estimated monthly sales per product)
dc_stock = pd.DataFrame({
    'Product': ['Frozen Croissant', 'Sliced Bread', 'Frozen Baguette', 'Chicken Nuggets', 
                'Pre-cooked Lasagna', 'Pastry Dough', 'Frozen Pizza', 'Cookies', 'Panettone', 'Instant Noodles', 
                'Hamburger Buns', 'Hot Dog Buns', 'Ready Cake'],
    'Stock': [11, 23, 32, 30, 13, 16, 22, 35, 32, 26, 10, 20, 30],
    'Monthly Sales': [44, 62, 90, 91, 27, 32, 101, 200, 80, 100, 41, 20, 91]
})

# Total quantity required to be shipped to the DC
total_requirement = 1200

# Initialize variables to control shipping and coverage period
shipment = []  # List to store the shipments made
coverage_months = 2  # Starts with 2 months of stock coverage in the DC
total_shipped = 0  # Total accumulated units shipped

# Main loop to perform product shipments until the total requirement is met
while total_shipped < total_requirement:
    for _, product in dc_stock.iterrows():
        name = product['Product']
        monthly_sales = product['Monthly Sales']
        current_stock = product['Stock']
        
        # Available stock in the industry for the current product
        industry_available_stock = industry_stock.loc[industry_stock['Product'] == name, 'Quantity']
        if not industry_available_stock.empty:
            industry_available_stock = industry_available_stock.values[0]
        else:
            continue  # Skip to the next product if the industry has no availability

        # Calculate the need to cover sales demand in the DC
        requirement = max(monthly_sales * coverage_months - current_stock, 0)
        shipped = min(requirement, industry_available_stock)  # Ship the minimum between the need and availability

        # Update stock in the industry and DC
        industry_stock.loc[industry_stock['Product'] == name, 'Quantity'] -= shipped
        dc_stock.loc[dc_stock['Product'] == name, 'Stock'] += shipped  # Update DC stock
        total_shipped += shipped  # Add shipped quantity to the total

        # Record the shipment made
        shipment.append({'Product': name, 'Shipped': shipped})

        # Break the loop if the total requirement is met
        if total_shipped >= total_requirement:
            break
    
    # Increase coverage for the next shipments, if the requirement has not yet been met
    coverage_months += 1

# Create a consolidated DataFrame with the shipments made by product
shipment_df = pd.DataFrame(shipment)
shipment_df = shipment_df.groupby('Product', as_index=False).sum()

# Adjust the total shipped to exactly match the total requirement (in case of excess)
if shipment_df['Shipped'].sum() > total_requirement:
    excess = shipment_df['Shipped'].sum() - total_requirement
    for i in range(len(shipment_df) - 1, -1, -1):  # Adjust shipments, starting from the last product
        if shipment_df.loc[i, 'Shipped'] > excess:
            shipment_df.loc[i, 'Shipped'] -= excess
            break
        else:
            excess -= shipment_df.loc[i, 'Shipped']
            shipment_df.loc[i, 'Shipped'] = 0
    shipment_df = shipment_df[shipment_df['Shipped'] > 0]  # Remove items with zero shipment after adjustment

# Display the final shipment result
print("Shipment to the DC (Total Shipped = {}):".format(shipment_df['Shipped'].sum()))
print(shipment_df)

# Display updated industry stock after shipment
print("\nUpdated Industry Stock:")
print(industry_stock)

# Display updated DC stock after shipment
print("\nUpdated DC Stock:")
print(dc_stock[['Product', 'Stock']])  # Show only updated DC stocks

# Export the results to an Excel file
output_file = r"C:\Users\alves\OneDrive\Desktop\python-projects\shipping_schedule.xlsx"
with pd.ExcelWriter(output_file) as writer:
    shipment_df.to_excel(writer, sheet_name="DC Shipments", index=False)
    dc_stock.to_excel(writer, sheet_name="Updated DC Stock", index=False)
    industry_stock.to_excel(writer, sheet_name="Updated Industry Stock", index=False)

print(f"Excel file successfully generated: {output_file}")
