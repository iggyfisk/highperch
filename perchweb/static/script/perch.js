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

			const ctx = cnv.getContext('2d');
			const mSize = cnv.clientWidth;
			cnv.height = cnv.width = mSize;

			// It doesn't start great
			const xDiff = mapSize.maxX - mapSize.minX;
			const yDiff = mapSize.maxY - mapSize.minY;
			const maxDiff = Math.max(xDiff, yDiff);

			// Gets worse
			const yScale = yDiff / maxDiff;
			const xScale = xDiff / maxDiff;
			const yOffset = mSize - (mSize * yScale);
			const xOffset = mSize - (mSize * xScale);

			const getCoords = t => {
				// Completely off the rails
				x = t[0] - mapSize.minX;
				xPct = x / xDiff;
				x = xPct * mSize;
				x = x + (xOffset / 2);

				y = t[1] - mapSize.minY;
				yPct = y / yDiff;
				y = yPct * (mSize * yScale);
				y = y + (yOffset / 2);
				y = mSize - y;

				return [x, y]
			}

			// Todo: Draw chunks of time based on replay timestamps
			let queue = 0;
			const animate = () => {
				if (queue) return;

				cnv.classList.toggle('anim');
				ctx.clearRect(0, 0, cnv.width, cnv.height);

				for (let [color, towers] of Object.entries(playerTowers)) {
					const drawNext = i => {
						coords = getCoords(towers[i]);
						ctx.fillStyle = color;						
						ctx.fillRect(coords[0] - po, coords[1] - po, ps, ps);

						if (towers.length > ++i) {
							setTimeout(drawNext.bind(this, i), 100);
						} else if (--queue == 0) {
							cnv.classList.toggle('anim');
						}
					}
					if (towers.length) {
						++queue;
						setTimeout(drawNext.bind(this, 0), 1);
					}
				}
			}

			if (cnv.classList.contains('anim')) {
				// Will have to bite the bullet and add something to the DOM instead
				ctx.font = "40px Scada";
				ctx.fillStyle = '#EEE';
				ctx.fillText("▶", (mSize / 2) - 15, (mSize / 2) + 15);

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


