from smart_claims.refund_flow import ClaimRefundFlow

def run():
    customer_claim = {
        "customer_id": "12345",
        "order_id": "67890",
        "order_date": "2022-01-01",
        "claim_date": "2022-03-31",
        "product_id": "P123",
        "product_name": "Panda Stuffed Animal",
        "product_cost": 50.0,
        "product_review": "The Panda is cute but it is damaged. There are scratches on the eyes, and stiches are broken leaving the cotton inside exposed.",
        "product_images": ["test/data/images/image1.jpg", "test/data/images/image2.jpg", "test/data/images/image3.jpg"]
    }
    
    flow = ClaimRefundFlow()
    final_output = flow.kickoff(inputs=customer_claim)

    print("---- Final Output ----")
    print(final_output)