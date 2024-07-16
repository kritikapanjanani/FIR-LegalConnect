// app.js

document.addEventListener('DOMContentLoaded', () => {
    const aboutUsHeading = document.querySelector('.about-us');
    const aboutUsPara = document.querySelector('.para-about-us');
  
    const options = {
      threshold: 0.5
    };
  
    const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.animationPlayState = 'running';
        } else {
          entry.target.style.animationPlayState = 'paused';
        }
      });
    }, options);
  
    observer.observe(aboutUsHeading);
    observer.observe(aboutUsPara);
  });