// code for index page image slider

document.addEventListener('DOMContentLoaded', ()=>{
    const resulttemplate = Handlebars.compile(document.querySelector('#resultHandlebar').innerHTML);
    var resultsArray = []
    document.querySelector('#searchinputfield').onkeyup = ()=>{
        
        const text = document.querySelector('#searchinputfield').value;
        if(text=='')   
            resultsArray = []
        //elements = document.getElementsByClassName('.relatedresults');
        
        fetch(`/searchforproduct?text=${text}`)
        .then(response => response.json())
        .then(data =>{
            //alert(resultsArray);
            if(data.relatedresults == '[]')
                document.querySelector('#relatedresultsdiv').innerHTML = '';
            else{
                // alert(data.relatedresults);
                resultsArray.splice(0,resultsArray.length);
                document.querySelector('#relatedresultsdiv').innerHTML = '';
                for (i in data.relatedresults){
                    //if(!resultsArray.includes(i)){
                        document.querySelector('#relatedresultsdiv').innerHTML += resulttemplate({'name':data.relatedresults[i]});
                    //}
            }
        }
        })
    }
})

function setinput(anc){
    //alert(anc.innerHTML);
    document.querySelector('#searchinputfield').value = anc.innerHTML;
}



let slideIndex = 0;


function showSlides() {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slideIndex++;
    if (slideIndex > slides.length) { slideIndex = 1 }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
    setTimeout(showSlides, 1800); // Change image every 2 seconds
}

//function to change image on location search page
function changeImage() {
    var imagesArr = ["url(../../static/loc5.jpg)", "url(../../static/loc8.jpg)", "url(../../static/loc9.jpg)", "url(../../static/loc10.jpg)", "url(../../static/fresh_fruits.jpg)"]
    var imagediv = document.getElementById("imagediv");
    var arrlength = imagesArr.length;
    var i = Math.floor(Math.random() * 4);
    imagediv.style.backgroundImage = imagesArr[i];

}

function showImage(img) {
    document.getElementById("productMainImage").src = img.src;
}

