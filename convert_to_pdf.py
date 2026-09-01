import os
import time
import comtypes.client

def convert_pptx_to_pdf(input_name="CYVERGE_SIH_2026_Vanguard_GWM.pptx", output_name="Vanguard_GWM_SIH_Submission.pdf"):
    print("🔄 Initializing PowerPoint application for clean PDF rendering...")
    
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = 1
    
    abs_in = os.path.abspath(input_name)
    abs_out = os.path.abspath(output_name)
    
    if not os.path.exists(abs_in):
        print(f"❌ Error: Could not find presentation file at {abs_in}")
        powerpoint.Quit()
        return

    deck = powerpoint.Presentations.Open(abs_in)
    time.sleep(2)
    
    deck.SaveAs(abs_out, 32)
    deck.Close()
    powerpoint.Quit()
    
    print(f"✅ Successfully generated clean PDF: {abs_out}")

if __name__ == "__main__":
    convert_pptx_to_pdf()
