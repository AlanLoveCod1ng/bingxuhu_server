const main = document.getElementById('main');
const filter = document.getElementById('blur-filter');

main.addEventListener('mouseover',() => filter.classList.add('blur'));
main.addEventListener('mouseleave',()=>filter.classList.remove('blur'));