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
			if (!fileName.match(/^Replay_\d{4}_/g) && fileName.slice(0, -4).length >= 6) {
				replayTitle.value = fileName.slice(0, -4).slice(0, 50);
			}
			replayTitle.focus();
			replayTitle.select();
		});
	});
})();

/* hp-toggle */
(() => {
	document.addEventListener("DOMContentLoaded", () => {
		document.querySelectorAll('.hp-toggle').forEach(el => {
			const { group } = el.dataset;
			const toggleClass = el.dataset.class || 'hidden';
			el.addEventListener('click', () => {
				document.querySelectorAll(`.hp-toggle[data-group="${group}"]`).forEach(e => {
					if (e.classList.contains('hp-control')) return;
					e.classList.toggle(toggleClass);
				});
			});
		});
	});
})();

/* Inaccuracy warning toggle */
(() => {
	document.addEventListener("DOMContentLoaded", () => {
		let inaccurateStatsOpen = 0;
		document.querySelectorAll('.inaccurate').forEach(el => {
			const open = parseInt(el.dataset.inaccurate);
			el.addEventListener('click', () => {
				inaccurateStatsOpen += open;
				document.querySelectorAll('.statwarning').forEach(e =>
					inaccurateStatsOpen ? e.classList.remove('hidden') : e.classList.add('hidden')
				);
			});
		});
	});
})();

/* Minimap drawings */
(() => {
	// Loads the image files even if they don't need to be drawn,
	// but on the other hand it starts loading and caching immediately.
	const goldImg = new Image();;
	goldImg.src = '/static/images/drawmap_mine.png';
	const playImg = new Image();
	playImg.src = '/static/images/drawmap_play.png';

	// There's a race condition where it will draw transparent images
	// if they're not loaded before drawing
	const imagesReady = (mapImg = { complete: true, addEventListener: () => {} }) => {
		const images = [ goldImg, playImg, mapImg];
		if (images.every(i => i.complete)) return Promise.resolve();

		return new Promise(resolve => {
			images.forEach(img => {				
				img.addEventListener('error', resolve);
				img.addEventListener('load', () => {
					if (images.every(i => i.complete)) resolve();
				});
			});
		});
	};

	document.addEventListener("DOMContentLoaded", () => {
		document.body.querySelectorAll('.drawmap').forEach(async cnv => {
			const mapSize = JSON.parse(cnv.dataset.mapsize);
			const playerTowers = JSON.parse(cnv.dataset.towers || '{}');
			const playerLocations = JSON.parse(cnv.dataset.startlocations || '{}');
			const goldMines = JSON.parse(cnv.dataset.mines || '[]');
			const animated = cnv.classList.contains('anim');
			const delayed = cnv.classList.contains('delay');
			const mapImg = delayed
				? cnv.parentNode.querySelector('img')
				: undefined;

			// Tower and start location size
			const ps = cnv.dataset.paintsize;
			const po = ps / 2;
			// Goldmine size
			const gs = ps * 3;
			const go = gs / 2;

			// Turn camera bounds into minimap bounds
			mapSize[0] -= 504;
			mapSize[1] += 504;
			mapSize[2] -= 248;
			mapSize[3] += 248;

			// Wait for map image to load and grow to real size when necessary
			if (delayed) await imagesReady(mapImg);

			const mapImageSize = cnv.clientWidth;
			const xSize = mapSize[1] - mapSize[0];
			const ySize = mapSize[3] - mapSize[2];
			const maxSize = Math.max(xSize, ySize);
			const scale = mapImageSize / maxSize;

			const xStart = -(xSize / maxSize * mapImageSize - mapImageSize) / 2;
			const yStart = -(ySize / maxSize * mapImageSize - mapImageSize) / 2;

			const getCoords = t => ([
				Math.round((t[0] - mapSize[0]) * scale + xStart),
				Math.round(mapImageSize - ((t[1] - mapSize[2]) * scale + yStart))]);

			cnv.height = cnv.width = mapImageSize;
			const ctx = cnv.getContext('2d');

			const drawBase = () => {
				goldMines.forEach(m => {
					const c = getCoords(m);
					ctx.drawImage(goldImg, c[0] - go, c[1] - go, gs, gs);
				});
				
				for (let [color, start] of Object.entries(playerLocations)) {
					ctx.fillStyle = color;
					const c = getCoords(start);
					ctx.fillRect(c[0] - ps, c[1] - ps, ps * 2, ps * 2);
				}
			}

			const animate = towers => {
				if (!cnv.classList.contains('anim')) return;
				cnv.classList.remove('anim');

				ctx.clearRect(0, 0, cnv.width, cnv.height);
				drawBase();

				// Fixed delay between each paint, but adjusted per replay, 15 - 250ms;
				const frameDelay = Math.round(Math.max(Math.min(10000 / towers.length, 250), 15));
				const drawNext = (i) => {
					ctx.fillStyle = towers[i][3];
					coords = getCoords(towers[i++]);
					ctx.fillRect(coords[0] - po, coords[1] - po, ps, ps);

					if (i < towers.length) {
						setTimeout(drawNext.bind(this, i), frameDelay);
					} else {
						cnv.classList.add('anim');
					}
				}
				setTimeout(drawNext.bind(this, 0), 1);
			}

			// Always wait for asset images to load before drawing them,
			// also wait for the map image to load when necessary
			if (animated || delayed) await imagesReady(mapImg);

			drawBase();
			if (animated) {
				// Animated minimap
				ctx.fillStyle = '#000C';
				ctx.fillRect((mapImageSize / 2) - 30, (mapImageSize / 2) - 30, 60, 60);
				ctx.drawImage(playImg, (mapImageSize / 2) - 25, (mapImageSize / 2) - 25, 50, 50);

				// Combine all players' towers and put them in order
				const orderedTowers = Object.entries(playerTowers)
					.map(([c, towers]) => towers.map(t => [...t, c]))
					.flat(1).sort((a, b) => (a[2] - b[2]));

				cnv.addEventListener('click', () => animate(orderedTowers));
			} else {
				// Simple minimap
				for (let [color, towers] of Object.entries(playerTowers)) {
					ctx.fillStyle = color;
					towers.map(getCoords).forEach(c => { ctx.fillRect(c[0] - po, c[1] - po, ps, ps) });
				}
			}
		});
	});
})();


