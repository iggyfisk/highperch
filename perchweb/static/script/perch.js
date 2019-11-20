/* Nav submenu START */
(() => {
	document.addEventListener("DOMContentLoaded", () => {
		const nav = document.querySelector('nav');
		nav.querySelector('span.submenu').addEventListener('click', event => {
			event.target.classList.toggle('active');
			event.target.textContent = event.target.textContent === '▼'
				? '▲'
				: '▼';
			nav.classList.toggle('expanded');              
		});
	});

})();
/* Nav submenu END */

/* Background switching START */
(() => {
	const cookie_name = 'HP_bg';
	document.addEventListener("DOMContentLoaded", () => {
		const html = document.querySelector('html');
		document.querySelectorAll('ul img.action').forEach(element => {
			element.addEventListener('click', event => {
				const bgStyle = event.target.dataset.bg;
				html.removeAttribute('class');
				html.setAttribute('class', bgStyle);
				document.body.removeAttribute('class');
				document.body.setAttribute('class', bgStyle);
				// 50 year anniversary
				document.cookie = cookie_name + '=' + bgStyle + '; expires=Mon, 01 Jun 2054 12:00:00 UTC';
			});
		});
	});
})();
/* Background switching END */