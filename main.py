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

# TODO: Integrate the Gradio Interface with the ClaimRefundFlow
# Function to process user inputs
def process_input(customer_id, order_id, order_date, claim_date, product_id, 
                  product_name, product_description, product_cost, product_review, product_images):
    
    # Simple response to show received data
    # TODO: Make Image format Compatible with Backend
    customer_claim = {
        "customer_id": customer_id,
        "order_id": order_id,
        "order_date": order_date,
        "claim_date": claim_date,
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
            gr.Textbox(label="Customer ID", placeholder="Enter Customer ID", type="text"),
            gr.Textbox(label="Order ID", placeholder="Enter Order ID", type="text"),
            gr.DateTime(label="Order Date"),  # Date input for order date
            gr.DateTime(label="Claim Date"),  # Date input for claim date
            gr.Textbox(label="Product ID", placeholder="Enter Product ID", type="text"),
            gr.Textbox(label="Product Name", placeholder="Enter Product Name", type="text"),
            gr.Textbox(label="Product Description", placeholder="Enter Product Description", type="text"),
            gr.Number(label="Product Cost"),
            gr.Textbox(label="Product Review", placeholder="Enter Product Review", type="text"),
            gr.Image(type="pil", label="Upload Product Images")  
        ],
        outputs=gr.JSON(label="Claim Details Output"),  
        live=False,
        submit_btn="Submit Claim",
        title="Claim Refund Agent",
    )

    iface.launch()
