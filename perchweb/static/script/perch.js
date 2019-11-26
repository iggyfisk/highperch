/* hp-expand START */
(() => {
	document.addEventListener("DOMContentLoaded", () => {
		document.querySelectorAll('.hp-expand').forEach(expEl=> {
			expEl.addEventListener('click', event => {
				event.target.classList.toggle('active');
				event.target.parentNode.querySelector('.hp-hidden').classList.toggle('visible');           
			});
		});
	});
})();
/* hp-expand END */

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
				document.cookie = cookie_name + '=' + bgStyle + ';path=/;expires=Mon, 01 Jun 2054 12:00:00 UTC';
			});
		});
	});
})();
/* Background switching END */

/* Replay title prepopulate START */
(() => {
	document.addEventListener("DOMContentLoaded", () => {
		var replayUploader = document.getElementById( 'uploader' );
		var replayTitle = document.getElementById( 'upload_namer' );
		if (replayUploader == null || replayTitle == null) {
			return;
		}
		replayUploader.addEventListener( 'change', event => {
			var input = event.srcElement;
			var fileName = replayUploader.files[0].name;
			if (!fileName.match(/^Replay_\d{4}_/g)) {
				replayTitle.value = fileName.slice(0, -4).slice(0, 50);
				}
			replayTitle.focus();
			replayTitle.select();
			}
		);
	});
})();
/* Replay title prepopulate END */
