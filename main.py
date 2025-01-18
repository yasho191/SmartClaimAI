from smart_claims.refund_flow import ClaimRefundFlow
import gradio as gr


# test data for reference
# customer_claim = {
#     "customer_id": "12345",
#     "order_id": "67890",
#     "order_date": "2022-01-01",
#     "claim_date": "2022-03-31",
#     "product_id": "P123",
#     "product_name": "Panda Stuffed Animal",
#     "product_description": "A cute stuffed animal in the shape of a Panda",
#     "product_cost": 50.0,
#     "product_review": "The Panda is cute but it is damaged. There are scratches on the eyes, and stiches are broken leaving the cotton inside exposed.",
#     "product_images": ["test/data/images/image1.jpg", "test/data/images/image2.jpg", "test/data/images/image3.jpg"]
# }

def validate_form_data(customer_id, order_id, order_date, claim_date, product_id, 
                  product_name, product_description, product_cost, product_review, product_images):
    
    if not customer_id:
        raise gr.Error("Customer ID cannot be empty")
    if not order_id:
        raise gr.Error("Order ID cannot be empty")
    if not order_date:
        raise gr.Error("Order Date cannot be empty")
    if not claim_date:
        raise gr.Error("Claim Date cannot be empty")
    if not product_id:
        raise gr.Error("Product ID cannot be empty")
    if not product_name:
        raise gr.Error("Product Name cannot be empty")
    if not product_description:
        raise gr.Error("Product Description cannot be empty")
    if not product_cost:
        raise gr.Error("Product Cost cannot be empty")
    if not product_review:
        raise gr.Error("Product Review cannot be empty")
    if not product_images:
        raise gr.Error("Product Images cannot be empty")
    
    
# TODO: Integrate the Gradio Interface with the ClaimRefundFlow
# Function to process user inputs
def process_input(customer_id, order_id, order_date, claim_date, product_id, 
                  product_name, product_description, product_cost, product_review, product_images):
    
    validate_form_data(customer_id, order_id, order_date, claim_date, product_id, 
                  product_name, product_description, product_cost, product_review, product_images)
    
    product_images = [image[0] for image in product_images]
    
    customer_claim = {
        "customer_id": customer_id,
        "order_id": order_id,
        "order_date": str(order_date),
        "claim_date": str(claim_date),
        "product_id": product_id,
        "product_name": product_name,
        "product_description": product_description,
        "product_cost": product_cost,
        "product_review": product_review,
        "product_images": product_images
    }
    
    # Constructing the returned data in the same format
    flow = ClaimRefundFlow()
    final_output = flow.kickoff(inputs=customer_claim)

    return final_output

if __name__ == "__main__":
    
    # Create the Gradio Interface with structured input fields
    iface = gr.Interface(
        fn=process_input,
        inputs=[
            gr.Textbox(value="123", label="Customer ID", placeholder="Enter Customer ID", type="text"),
            gr.Textbox(value="2", label="Order ID", placeholder="Enter Order ID", type="text"),
            gr.DateTime(label="Order Date"),  # Date input for order date
            gr.DateTime(label="Claim Date"),  # Date input for claim date
            gr.Textbox(value="34", label="Product ID", placeholder="Enter Product ID", type="text"),
            gr.Textbox(label="Product Name", placeholder="Enter Product Name", type="text"),
            gr.Textbox(label="Product Description", placeholder="Enter Product Description", type="text"),
            gr.Number(value=1, label="Product Cost", minimum=1, precision=2),
            gr.Textbox(label="Product Review", placeholder="Enter Product Review", type="text"),
            gr.Gallery(type="str", file_types=[".png", ".jpg", ".jpeg"], label="Upload Product Images")  
        ],
        outputs=gr.JSON(label="Claim Details Output"),  
        live=False,
        submit_btn="Submit Claim",
        title="Claim Refund Agent",
    )

    iface.launch()
