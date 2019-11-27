/* hp-expand */
(() => {
	document.addEventListener("DOMContentLoaded", () => {
		document.querySelectorAll('.hp-expand').forEach(expEl => {
			expEl.addEventListener('click', event => {
				let parent = event.target.parentNode;
				let expandTarget = null;
				// Recursively look for a .hp-hidden element to expand
				while (!(expandTarget = parent.querySelector('.hp-hidden')) && parent !== document.body) {
					parent = parent.parentNode;
				}
				if (expandTarget) {
					event.target.classList.toggle('active');
					expandTarget.classList.toggle('visible');
				}
			});
		});
	});
})();

/* Background switching */
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

/* Replay title prepopulate */
(() => {
	document.addEventListener("DOMContentLoaded", () => {
		const replayUploader = document.getElementById('uploader');
		const replayTitle = document.getElementById('upload_namer');
		if (!replayUploader || !replayTitle) return;
		replayUploader.addEventListener('change', () => {
			const fileName = replayUploader.files[0].name;
			if (!fileName.match(/^Replay_\d{4}_/g)) {
				replayTitle.value = fileName.slice(0, -4).slice(0, 50);
			}
			replayTitle.focus();
			replayTitle.select();
		});
	});
})();

/* Minimap drawings */
(() => {
	document.addEventListener("DOMContentLoaded", () => {
		document.body.querySelectorAll('.drawmap').forEach(cnv => {
			const playerTowers = JSON.parse(cnv.dataset.towers);
			const mapSize = JSON.parse(cnv.dataset.mapsize);
			const ps = cnv.dataset.paintsize;
			const po = ps / 2;

			const mapImageSize = cnv.clientWidth;
			const xSize = mapSize.maxX - mapSize.minX;
			const ySize = mapSize.maxY - mapSize.minY;
			const maxSize = Math.max(xSize, ySize);
			const scale = mapImageSize / maxSize;

			const xStart = -(xSize / maxSize * mapImageSize - mapImageSize) / 2;
			const yStart = -(ySize / maxSize * mapImageSize - mapImageSize) / 2;

			const getCoords = t => ([
				(t[0] - mapSize.minX) * scale + xStart,
				mapImageSize - ((t[1] - mapSize.minY) * scale + yStart)]);
		
			cnv.height = cnv.width = mapImageSize;
			const ctx = cnv.getContext('2d');
			let queue = 0;
			const animate = () => {
				if (queue) return;

				cnv.classList.toggle('anim');
				ctx.clearRect(0, 0, cnv.width, cnv.height);

				const frameDelay = 50;
				const frameLength = 10000;
				const startSkip = 60000;

				for (let [color, towers] of Object.entries(playerTowers)) {
					const drawNext = (i, time) => {
						console.log(color, time);
						ctx.fillStyle = color;
						while (i < towers.length && time >= towers[i][2]) {
							coords = getCoords(towers[i++]);
							ctx.fillRect(coords[0] - po, coords[1] - po, ps, ps);
						}

						if (i < towers.length) {
							setTimeout(drawNext.bind(this, i, time + frameLength), frameDelay);
						} else if (--queue == 0) {
							cnv.classList.toggle('anim');
						}
					}

					if (towers.length) {
						++queue;
						drawNext(0, startSkip);
					}
				}
			}

			if (cnv.classList.contains('anim')) {
				// Will have to bite the bullet and add something to the DOM instead
				ctx.font = "40px sans";
				ctx.fillText("▶️", (mapImageSize / 2) - 25, (mapImageSize / 2) + 15);
				cnv.addEventListener('click', animate);
			} else {
				for (let [color, towers] of Object.entries(playerTowers)) {
					ctx.fillStyle = color;
					towers.map(getCoords).forEach(c => { ctx.fillRect(c[0] - po, c[1] - po, ps, ps) });
				}
			}
		});
	});
})();


