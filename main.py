from smart_claims.refund_flow import ClaimRefundFlow
import gradio as gr
from datetime import date
import uuid


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
#     "product_review": "The Panda is cute but it is damaged. There are scratches on the eyes, and stitches are broken leaving the cotton inside exposed.",
#     "product_images": ["test/data/images/image1.jpg", "test/data/images/image2.jpg", "test/data/images/image3.jpg"]
# }

def validate_form_data(order_date, product_name, product_description, product_cost, product_review, product_images):
    
    if not order_date:
        raise gr.Error("Order Date cannot be empty")
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
def process_input(
        order_date, 
        product_name, 
        product_description, 
        product_cost, 
        product_review, 
        product_images
    ):
    
    validate_form_data(order_date, product_name, product_description, product_cost, product_review, product_images)
    
    customer_claim = {
        "customer_id": uuid.uuid4(),
        "order_id": uuid.uuid4(),
        "order_date": str(order_date),
        "claim_date": str(date.today()),
        "product_id": uuid.uuid4(),
        "product_name": product_name,
        "product_description": product_description,
        "product_cost": product_cost,
        "product_review": product_review,
        "product_images": [image[0] for image in product_images]
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
            gr.DateTime( label="Order Date", include_time=False),  # Date input for order date
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
