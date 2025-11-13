# HW2: Plotly + Streamlit - Sharing Your Work

## Goals
- Practice building Streamlit App with Streamlit and Plotly 
- Learn how to deploy and share a Streamlit app using Streamlit Cloud.
  
Resource: [streamlit](https://docs.streamlit.io/get-started/fundamentals/main-concepts)
> Instruction: This HW is light enough to be run locally. Run on your laptop instead of Farmshare. Clone your repo to your laptop.
---

## Part 1 - Streamlit features

To run the app:

```bash
streamlit run app.py
```
You will need to install packages in `requirement.txt`. Apply what you learn in Lecture 2 to set up your environment.

### Add a Logo or Header Image
At the very top of the Streamlit app, add an image as your app logo

```python
# TODO: Add a logo or image above the title, replace with your favorite image
st.image(
    "https://github.com/khoa-yelo/BIOS270-AU25/blob/main/Writeups/writeup0/snyderlab.png?raw=true",
    width=150
)
```
Try placing this before `st.title("Pairwise Sequence Aligner")`.

---

### Plot a Histogram of Match Values
After alignment is computed, visualize how many positions were matches (1) vs mismatches (0).

```python
# TODO: Find an appropriate location in `app.py` to insert this code
fig = px.histogram(vals, nbins=10, title="Distribution of Match Values (Match=1, Mismatch=0)")
st.plotly_chart(fig, use_container_width=True)
```

Run the app locally to make sure everything works as expected.

---

## Part 2 - Multiple Choice Questions

### Q1.  
In Streamlit, what happens when you define and click the defined button:
```python
align_clicked = st.button("▶️ Align sequences")
```

- [ ] The app runs this line only once when first loaded and won't rerun it.  
- [ ] The app waits (pauses) until the user clicks the button before continuing.  
- [ ] When the user clicks the button, Streamlit reruns the entire script from the top, and `align_clicked` becomes `True` for that run, allowing the code inside `if align_clicked:` to execute.  

---

### Q2.  
Why do we use:
```python
st.plotly_chart(fig, use_container_width=True)
```
- [ ] It makes the chart automatically scale to fit the available page width.  
- [ ] It forces Streamlit to display a smaller chart.  
- [ ] It changes how Plotly computes data ranges.  

---

## Part 3 — Share Your Streamlit App Online

### Step 1. Push your code to GitHub
Push your modified `app.py`.

### Step 2. Deploy to Streamlit Cloud
1. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)  
2. Click **“Deploying” (Free)** → Connect your GitHub account.  
3.  **Create App** -> Select your repo, branch (e.g. `main`), and main file (`app.py`), modify your `domain` name.  
4. Click **Deploy**.  
5. Wait for your app to build — it will give you a public URL like:
   https://bios270-au25-hw2-example.streamlit.app/


### Step 3. Test and Submit
Once your app is running:
- Test that it loads properly and alignment works.  
- Make sure the histogram and logo you inserted in **Part 1** appear.  

Then, copy and paste your **Streamlit Cloud URL** below  

```
Streamlit App URL:
https://____________________________________
```
Submit the `HW2.md` URL to **Canvas**.