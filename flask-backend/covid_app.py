from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import joblib
import os
app = Flask(__name__)

# === Load CSV file ===
df = pd.read_csv("flask-backend/COVID19_Coronavirus_Analyzer.csv")

# === Extract symptom columns ===
symptom_columns = [col for col in df.columns if col not in ["Age", "Gender", "class", "Disease", "Suggestion"]]

# === Load model and vectorizer ===
model = joblib.load("flask-backend/covid_model.pkl")
vectorizer = joblib.load("flask-backend/covid_vectorizer.pkl")


html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Disease Prediction</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background-color: #f4f4f4; 
            text-align: center; 
        }
       .container { 
    width: 60%; 
    height: auto; /* Adjust height dynamically */
    margin: 100px auto; /* Leaves space from header & footer */
    background: white; 
    padding: 20px; 
    border-radius: 10px; 
    box-shadow: 0px 0px 10px rgba(0,0,0,0.1); 
}

h2 { 
    color: #333; 
    font-size: 24px; /* Increased text size */
    text-align: center; /* Center the heading */
}

        form { 
            text-align: left; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
        }
       .symptom-group { 
    display: flex; 
    align-items: center; 
    justify-content: space-between; 
    width: 80%; 
    margin-bottom: 10px;  
    font-size: 18px; 
    padding: 12px;  
    background-color: #f9f9f9;  
    border-radius: 5px;  
    position: relative;  /* Ensures it stays correctly positioned */
    z-index: 100;  /* Ensures it stays above the header */
}


label { 
    flex: 1; 
    text-align: left; 
    font-weight: bold; /* Added bold for better visibility */
}

.options { 
    display: flex; 
    gap: 15px; 
    flex-wrap: wrap; /* Allows wrapping if space is limited */
}

.btn { 
    background-color: #007bff; 
    color: white; 
    padding: 12px 24px; /* Increased padding for better button size */
    border: none; 
    font-size: 18px; 
    cursor: pointer; 
    border-radius: 5px; 
    margin-top: 20px; 
    transition: background-color 0.3s ease; /* Smooth transition effect */
}

.btn:hover { 
    background-color: #0056b3; 
}

.result { 
    font-size: 20px; 
    color: #d9534f; 
    margin-top: 20px; 
    font-weight: bold; /* Added bold for better visibility */
}

        #more-info-btn { 
            display: none; 
            background-color:#007bff ; 
            color: white; 
            padding: 10px 20px; 
            border: none; 
            font-size: 18px; 
            cursor: pointer; 
            border-radius: 5px; 
            margin-top: 20px; 
        }
        #more-info-btn:hover { 
            background-color:#007bff; 
        }
          /* google font   */
  @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap');

  /* root color  */
  :root{
    --blue:#0188df;
    --black:#444d53;
    --wight:#fff;
  }

  /* custom css  */
  *{
    font-family: "Roboto", sans-serif;
    margin: 0; padding: 0;
    text-decoration: none;
    text-transform: capitalize;
    outline: none;
    box-sizing: border-box;
    transition: all linear .2s;
  }

  html{
    font-size: 62.5%;
    overflow-x: hidden;
  }

 /* button  */
 .button{
    height: 3.5rem;
    width: 15rem;
    background: var(--blue);
    color: var(--wight);
    font-size: 1.7rem;
    text-transform: capitalize;
    border-radius: .5rem;
    cursor: pointer;
    margin: 1rem 0;
    border: .1rem solid var(--blue);
 }

 .button:hover{
    border: .1rem solid var(--blue);
    background: var(--wight);
    color: var(--blue);
    letter-spacing: .2rem;
 }

 /* heading  */
.heading{
    text-align: center;
    font-size: 4rem;
    padding: 1rem;
    padding-top: 8rem;
    color: var(--blue);
    letter-spacing: .1rem;
}
 /* title  */
.title{
    text-align: center;
    padding: 0rem 1rem;
    font-size: 2.5rem;
    color: var(--black);
    font-weight: 300;
}



  /* header navbar section start  */

  header{
    width: 96%;
    background: var(--wight);
    position:fixed;
    top: 2rem;
    left: 50%;
    transform: translate(-50%);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 2rem;
    z-index: 1000;
  }

  /* logo name  */
  header a{
    color: var(--black);
  }

  header a:hover{
    color: var(--blue);
  }

  header .logo{
    font-size: 3rem;
  }

  header .logo span{
    color: var(--blue);
  }

  /* navbar link  */
  header .navbar ul{
    display: flex;
    align-items: center;
    justify-content: space-between;
    list-style: none;
  }

  header .navbar ul li{
    margin: 0 1rem;
  }

  header .navbar ul li a{
    font-size: 2rem;
    color: var(--black);
  }

  header .navbar ul li a:hover{
    color: var(--blue);
  }

 header .fa-bars{
    font-size: 3rem;
    color: var(--blue);
    cursor: pointer;
    display: none;
 }

 header .fa-times{
    transform: rotate(180deg);
 }


 .header-active{
    top: 0;
    width: 100%;
    box-shadow: .1rem .3rem rgba(0,0,0,.3);
 }



  /* header navbar section end  */

  /* home section start  */

  .home{
    min-height: 100vh;
    padding-top: 10rem;
  }

  .home .row{
    display: flex;
    align-items: center;
    justify-content: space-around;
    width: 85%;
    margin: 0 auto;
  }

  /* home images  */
  .home .row .images img{
    height: 75vh;
  }

  /* home heading  */
  .home .content h1{
    font-size: 4rem;
    color: var(--black);
  }

  .home .content h1 span{
    color: var(--blue);
  }

  .home .content p{
    font-size: 1.9rem;
    color: var(--black);
  }


  /* home section end  */


  /* about section start  */
  .about{
    background-color: #f9f9f9;
  }

  .about .box-container{
    padding: 4rem 0;
  }

  .about .box-container .box{
    width: 75%;
    margin: 4rem auto;
    border-radius: .5rem;
    box-shadow: 0 .3rem .5rem rgba(0,0,0,.3);
    display: flex;
    align-items: center;
    overflow: hidden;
    background: var(--wight);
  }

  /* about images  */
  .about .box-container .box .images{
    height: 40rem;
    width: 50%;
  }

  .about .box-container .box .images img{
    height: 100%;
    width: 100%;
  }

  /* about heading & text */
  .about .box-container .box .content{
    height: 100%;
    width: 50%;
    padding: 2rem;
  }

  .about .box-container .box .content h3{
    font-size: 3rem;
    color: var(--blue);
    display: flex;
    align-items: start;
  }

  .about .box-container .box .content p{
    font-size: 1.5rem;
    color: var(--black);
    padding: 1rem 0;
    text-align: start;
  }

  .about .box-container .box:nth-child(even){
    flex-flow: row-reverse;
  }
  

   /* about section end  */
  
  /* card section start  */

  .card .box-container{
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
  }

  .card .box-container .box{
    width: 30rem;
    margin: 2rem 1rem;
    overflow: hidden;
    border-radius: .5rem;
    box-shadow: 0 .3rem .5rem rgba(0,0,0,.3);
  }

  /* card images  */
  .card .box-container .box img{
    height: 30rem;
    width: 100%;
    object-fit: cover;
  }

  .card .box-container .box .content{
    padding: 1rem 1.3rem;
  }

  .card .box-container .box .content h2{
    font-size: 2rem ;
    text-align: center;
    color: var(--black);
  }

  .card .box-container .box .content h2:hover{
    color: var(--blue);
    text-decoration: underline;
  }

  .card .box-container .box .content p{
    font-size: 1.7rem;
    text-align: center;
    color: var(--black);
  }

  .card .box-container .box .content .icons{
    text-align: center;
  }
  
  .card .box-container .box .content .icons a{
    font-size: 2rem;
    color: var(--blue);
    text-align: center;
    margin: 1rem;
  }
  /* card section end  */

  /* review section start  */
  .review .box-container{
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    padding: 2rem 0;
  }

  .review .box-container .box{
    width: 35rem;
    text-align: center;
    padding: 0 2rem;
    margin: 4rem 1.5rem;
    box-shadow: 0 .3rem .5rem rgba(0,0,0,.3);
  }

  /* images  */
  .review .box-container .box .images{
    display: flex;
    align-items: center;
    text-align: left;
    padding: .5rem 0;
    border-top: .1rem solid #333;
  }

  .review .box-container .box .images img{
    height: 9rem;
    width: 9rem;
    border-radius: 50%;
    object-fit: cover;
    margin: .8rem 1rem;
  }

  .review .box-container .box i{
    font-size: 6rem ;
    margin-top: -3rem;
    color: var(--blue);
    opacity: .4;
  }

  
  .review .box-container .box p{
    color: var(--black);
    font-size: 1.7rem;
    padding: 2rem 0;
  }

  .review .box-container .box .info h3{
    color: var(--blue);
    font-size: 2rem;
  }
  .review .box-container .box .info span{
    color: var(--black);
    font-size: 2rem;
  }
  /* review section end */

  /* contact section start  */
  .contact{
    background: #eee;
  }

  .contact .row{
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 5rem 0;
  }

  .contact .row .images img{
    width: 50vw;
    height: 70vh;
  }

  .contact .row  .form-container{
    width: 50%;
    padding-right: 6rem;
  }

  .contact .row  .form-container input, textarea{
    height: 4rem;
    width: 100%;
    background: var(--wight);
    border: none;
    border-radius: 5rem;
    padding: 0 1rem;
    margin: 1rem 0;
    color: var(--blue);
    font-size: 1.7rem;
  }

  .contact .row  .form-container input:focus , textarea:focus{
    border: .2rem solid var(--blue);
  }

  .contact .row  .form-container textarea{
    height: 20rem;
    border-radius: 1rem;
    padding: 1rem;
    resize: none;
  }

  .contact .row  .form-container input[type="submit"]{
    width: 17rem;
    background: var(--blue);
    color: var(--wight);
    cursor: pointer;
    font-size: 2rem;
  }

  .contact .row  .form-container input[type="submit"]:hover{
    background: var(--wight);
    color: var(--blue);
    border: .2rem solid var(--blue);
  }
  /* contact section end  */

  /* bolg section start  */
  .News .box-container{
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
  }

  .News .box-container .box{
    width: 35rem;
    margin: 2rem 1rem;
    overflow: hidden;
    border-radius: .5rem;
    box-shadow: 0 .3rem .5rem rgba(0,0,0,.3);
  }

  /* blog images  */
  .News .box-container .box img{
    width: 100%;
    object-fit: cover;
  }

  .News .box-container .box .content{
    padding: 0 1.5rem;
  }

  .News .box-container .box .content h2{
    font-size: 2rem;
    color: var(--blue);
  }

  .News .box-container .box .content p{
    font-size: 1.3rem;
    color: var(--black);
  }
  /* bolg section end  */

  /* footer section start  */
 .footer{
  background: var(--black);
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  padding: 2rem 0;
 }

 .footer .box{
  width: 30rem;
  margin: 2rem;
  text-align: center;
 }

 .footer .box:nth-child(1){
  text-align: left;
 }

/* logo  */

.footer .box .logo{
  padding: 2rem 0;
  font-size: 3rem;
  color: var(--wight);
}

.footer .box .logo:hover{
  color: var(--blue);
}

.footer .box .logo span{
  color: var(--blue);
}

.footer .box p{
  font-size: 1.5rem;
  color: var(--wight);
}

.footer .box a{
  color: var(--wight);
  font-size: 2rem;
  display: block;
  padding: .2rem 0;
}

.footer .box a:hover{
  text-decoration: underline;
}


.footer .credit{
  width: 85%;
  padding-top: 1rem;
  font-size: 2rem;
  color: var(--wight);
  text-align: center;
  border-top: .2rem solid var(--wight);
}

.footer .credit span{
  color: var(--blue);
  text-decoration: underline;
  letter-spacing: .5rem;
}



  /* footer section end  */









  /* media query  */

  @media (max-width:768px){

    html{
        font-size: 55%;
    }

    header .fa-bars{
        display: block;
    }
    
    header .navbar{
        position: fixed;
        top: -100rem; left: 0;
        width: 100%;
        background: var(--wight);
        opacity: 0;
    }

    header .navbar ul{
        flex-flow: column;
        padding: 2rem 0;
    }

    header .navbar ul li{
        margin: 1rem 0;
        width: 100%;
        text-align: center;
    }

    header .navbar ul li a{
        font-size: 3rem;
        display: block;
    }

    header .nav-toggle{
        top: 5.5rem;
        opacity: 1;
    }

    /* home media query  */

    .home .row{
        flex-flow: column;
    }

    .home .row .content{
        text-align: center;
    }

    /* home images  */
    .home .row .images img{
        width: 100%;
    }

  /* about media query  */
   .about .box-container .box{
    flex-flow: column;
    width: 90%;
   }

   .about .box-container .box:nth-child(even){
    flex-flow: column;
   }

   .about .box-container .box .images{
    width: 100%;
   }

   .about .box-container .box .content{
    width: 100%;
   }
   
   /* contact form  */
   .contact .row{
    flex-flow: column;
   }

   .contact .row .images img{
    height: 50vh;
    width: 90vw;
   }

   .contact .row .form-container{
    width: 90%;
    padding: 0;
   }


      
 /* Hide elements before Google Translate loads */
    iframe.goog-te-banner-frame,
    .goog-te-banner-frame,
    .skiptranslate,
    body > .skiptranslate {
      display: none !important;
      height: 0 !important;
      visibility: hidden !important;
    }

    body {
      top: 0px !important;
      position: relative !important;
    }

.goog-te-banner-frame,
  .goog-tooltip,
  .goog-text-highlight,
  .goog-te-balloon-frame {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
  }

  body {
    top: 0 !important;
  }
/* Make "Powered by Google Translate" text and logo white */
.goog-logo-link,
.goog-te-gadget span:not(.goog-te-menu-value) {
    color: white !important;
    filter: brightness(0) invert(1); /* Makes the logo white */
}
/* Overlay white box completely over the "Powered by" */
#google_translate_element .goog-te-gadget {
    position: relative;
    z-index: 1;
}

/* Left-aligned white overlay box */
#google_translate_element::after {
    content: "";
    position: absolute;
    bottom: 0;
    right: 0; /* Align to right */
    height: 2.2em;
    width: 13.5%;
    background-color: white;
    z-index: 2;
}




/* Ensure language dropdown remains visible */
.goog-te-gadget,
.goog-te-combo {
    display: inline-block !important;
    visibility: visible !important;
}






    </style>
    <script>
    document.addEventListener("DOMContentLoaded", function () {
        // Navbar Toggle Functionality
        document.querySelector(".fa-bars").addEventListener("click", function () {
            this.classList.toggle("fa-times");
            document.querySelector(".navbar").classList.toggle("nav-toggle");
        });

        // Scroll Event for Header Styling
        window.addEventListener("scroll", function () {
            document.querySelector(".fa-bars").classList.remove("fa-times");
            document.querySelector(".navbar").classList.remove("nav-toggle");

            if (window.scrollY > 30) {
                document.querySelector("header").classList.add("header-active");
            } else {
                document.querySelector("header").classList.remove("header-active");
            }
        });

        // Contact Form Submission
        document.getElementById("contactForm").addEventListener("submit", function (event) {
            event.preventDefault(); // Prevent default form submission

            // Get form values
            let name = document.getElementById("name").value.trim();
            let email = document.getElementById("email").value.trim();
            let phone = document.getElementById("phone").value.trim();
            let message = document.getElementById("message").value.trim();

            if (!name || !email || !phone || !message) {
                alert("Please fill in all fields before submitting.");
                return;
            }

            let formData = { name, email, phone, message };

            // Send data to backend
            fetch("/contact", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData),
            })
            .then(response => response.json())
            .then(data => {
                alert("Query sent successfully!");
                document.getElementById("contactForm").reset(); // Reset form after submission
            })
            .catch(error => {
                alert("Error submitting form. Please try again.");
                console.error("Submission Error:", error);
            });
        });
    });

    function predictDisease() {
        let symptoms = {};
        document.querySelectorAll("input[type=radio]:checked").forEach((input) => {
            symptoms[input.name] = input.value === "Yes" ? 1 : 0;
        });

        fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ symptoms: symptoms })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("disease").innerText = data.disease || "Error predicting disease";
            document.getElementById("suggestion").innerText = data.suggestion || "No suggestions available";

            // Show button only if disease is predicted
            document.getElementById("more-info-btn").style.display =
                data.disease && data.disease !== "Normal (No Disease)" ? "block" : "none";
        })
        .catch(error => console.error("Error:", error));
    }
</script>

</head>
<body>
    <body>

  <!-- header navbar section start  -->

    <header>
        <a href="#" class="logo"><b><span>M</span>edi - <span>C</span>ares.</b></a>

        <nav class="navbar">
            <ul>
                <li><a href="index.html">home</a></li>
                <li><a href="index.html#about">about</a></li>
                <li><a href="index.html#Vitality">Vitality</a></li>
                <li><a href="index.html#review">Reviews</a></li>
                <li><a href="index.html#News">News</a></li>
                  <li><a href="index.html#contact">contact</a></li>
                 

            </ul>
        </nav>

        <div class="fas fa-bars"></div>
    </header>

<!-- Google Translate Init -->
<div id="google_translate_element" style="display: none;"></div>

<!-- Google Translate Script -->
<script src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>

<script type="text/javascript">
  function googleTranslateElementInit() {
    new google.translate.TranslateElement({ pageLanguage: 'en' }, 'google_translate_element');
  }

  function removeGoogleTranslateElements() {
    // Remove banner and top bar
    const bannerFrame = document.querySelector('iframe.goog-te-banner-frame');
    const skipTranslate = document.querySelector('.skiptranslate');
    const balloonItems = document.querySelectorAll('.goog-te-balloon-frame, .goog-tooltip, .goog-text-highlight');

    if (bannerFrame) bannerFrame.style.display = 'none';
    if (skipTranslate) skipTranslate.style.display = 'none';
    if (document.body) document.body.style.top = '0px';

    // Remove translation balloon/popups
    balloonItems.forEach(el => el.remove());
  }

  window.addEventListener('load', () => {
    // Run cleanup immediately and repeatedly
    const interval = setInterval(removeGoogleTranslateElements, 500);
    setTimeout(() => clearInterval(interval), 10000); // Stop after 10s

    // Optional: Watch for dynamic DOM changes
    const observer = new MutationObserver(removeGoogleTranslateElements);
    observer.observe(document.body, { childList: true, subtree: true });
  });
</script>


 <div class="container"><br><br><br>
        <h2 style="font-size: 3.2rem; color: #0188df;">COVID19 (coronavirus) Analyzer</h2><br><br>
        <h3 style="font-size: 2.3rem">Please Answer Yes/No For The Symptoms Below:</h3><br><br><br><br>

        <form id="symptomForm">
            <div class="symptom-group">
                <label><b>Age</b></label>
                <div class="options">
                    <input type="number" name="Age" required>
                </div>
            </div>

            <div class="symptom-group">
                <label><b>Gender</b></label>
                <div class="options">
                    <select name="Gender" required>
                        <option value="">Select</option>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                    </select>
                </div>
            </div>

            {% for symptom in symptoms %}
            <div class="symptom-group">
                <label><b>{{ symptom }}</b></label>
                <div class="options">
                    <input type="radio" name="{{ symptom }}" value="Yes" required> Yes
                    <input type="radio" name="{{ symptom }}" value="No" required> No
                </div>
            </div>
            {% endfor %}

            <button class="btn" type="submit">Predict</button>
        </form><br><br><br>

        <div class="result" id="result">
            <p><b>Positive/Negative:</b> <span id="Prediction"></span></p><br><br>
            <p><b>Prediction:</b> <span id="Disease"></span></p><br><br>
            <p><b>Suggestion:</b> <span id="Suggestion"></span></p><br><br><br>
           
        </div>
    </div>

    <script>
        document.getElementById("symptomForm").addEventListener("submit", async function (event) {
            event.preventDefault();

            const form = document.getElementById("symptomForm");
            const formData = new FormData(form);
            const data = {};

            formData.forEach((value, key) => {
                data[key] = value;
            });

            try {
                const response = await fetch("/predict", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ symptoms: data })
                });

                const result = await response.json();

                if (result.error) {
                    alert("Error: " + result.error);
                } else {
                    document.getElementById("Prediction").textContent = result.Prediction;
                    document.getElementById("Disease").textContent = result.Disease;
                    document.getElementById("Suggestion").textContent = result.Suggestion;
                    document.getElementById("result").style.display = "block";
                }
            } catch (error) {
                console.error("Prediction failed:", error);
                alert("Something went wrong while predicting the disease.");
            }
        });
    </script>




    
     <!-- Footer Section Start -->
    <section class="footer">
        <div class="box">
            <h2 class="logo"><span>M</span>edi - <span>C</span>ares</h2>
            <p>Your Trusted Health Companion.<br> Explore it!</p>
        </div>

        <div class="box">
            <h2 class="logo"><span>S</span>hare</h2>
            <a href="#"><i class="fab fa-facebook"></i> medicare</a>
            <a href="#"><i class="fab fa-twitter"></i> @medicare</a>
            <a href="#"><i class="fab fa-instagram"></i> medi_care</a>
            <a href="#"><i class="fab fa-pinterest"></i> medi-care.com</a>
        </div>

        <div class="box">
            <h2 class="logo"><span>L</span>inks</h2>
            <a href="index.html">home</a>
            <a href="index.html#about">about</a>
            <a href="index.html#Vitality">Vitality</a>
            <a href="index.html#contact">contact</a>
            <a href="index.html#News">News</a>
        </div>

        <h1 class="credit">@Medi-Care <br> All rights reserved.</h1>
    </section>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(html_template, symptoms=symptom_columns)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        if request.is_json:
            data = request.get_json()
            symptoms_data = data.get("symptoms", {})
        else:
            symptoms_data = request.form.to_dict()

        # Ensure we check only the known symptom columns
        selected_symptoms = [symptom for symptom in symptom_columns if symptoms_data.get(symptom, "").lower() == "yes"]

        print("Selected symptoms:", selected_symptoms)  # 🔍 Debug

        # 🔒 If no symptoms OR less than 3 symptoms, return "Negative"
        if len(selected_symptoms) < 3:
            return jsonify({
                "Prediction": "Negative",
                "Disease": "None",
                "Suggestion": "No COVID19 detected. Maintain a healthy lifestyle. Consult a general physician if symptoms persist."
            })

        # 🧠 Vectorize symptoms
        symptom_text = ", ".join(selected_symptoms)
        symptoms_vector = vectorizer.transform([symptom_text])

        # 🎯 Predict with the model
        prediction_class = model.predict(symptoms_vector)[0].strip().lower()

        # 🔍 Match with the dataset
        match = df[df["Disease"].str.strip().str.lower() == prediction_class]

        if not match.empty:
            disease_type = match["Disease"].mode()[0]
            suggestion = match["Suggestion"].mode()[0]
            diagnosis_class = "Positive"
        else:
            disease_type = "Unknown"
            suggestion = "No suggestion available"
            diagnosis_class = "Positive"

        return jsonify({
            "Prediction": diagnosis_class,
            "Disease": disease_type,
            "Suggestion": suggestion
        })

    except Exception as e:
        print("🔥 Error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5003))  # Render provides PORT dynamically
    app.run(host="0.0.0.0", port=port, debug=True)

