const signup = document.querySelector("#signup_link");
const signin = document.querySelector("#signin_link");
const signout = document.querySelector("#signout_link");
const myinfo = document.querySelector("#myinfo_link");
const createArticleLink = document.querySelector("#create_article_link");


function showAndHideNavbarMenu(){
    let authtoken = window.sessionStorage.getItem("authtoken");

    if (authtoken){
        signup.style.display= "none";
        signin.style.display= "none";

    }
    else{
        signout.style.display= "none";
        myinfo.style.display= "none";
        createArticleLink.style.display = "none";
    }
}

window.addEventListener("load", showAndHideNavbarMenu);

function signOutHandler(){
    window.sessionStorage.removeItem("authtoken");
    window.sessionStorage.removeItem("username");

    let url = '/home';
    window.location.replace(url);
}


signout.addEventListener("click", signOutHandler);



