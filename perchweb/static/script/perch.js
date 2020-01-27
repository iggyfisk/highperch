const neutralBuildingCodes = {
	'ngol': 'Gold Mine',
	'ntav': 'Tavern',
	'ngme': 'Goblin Merchant',
	'ngad': 'Goblin Laboratory',
	'nmer': 'Mercenary Camp (Lordaeron Summer)',
	'nmr0': 'Mercenary Camp (Village)',
	'nmr2': 'Mercenary Camp (Lordaeron Fall)',
	'nmr3': 'Mercenary Camp (Lordaeron Winter)',
	'nmr4': 'Mercenary Camp (Barrens)',
	'nmr5': 'Mercenary Camp (Ashenvale)',
	'nmr6': 'Mercenary Camp (Felwood)',
	'nmr7': 'Mercenary Camp (Northrend)',
	'nmr8': 'Mercenary Camp (Cityscape)',
	'nmr9': 'Mercenary Camp (Dalaran)',
	'nmra': 'Mercenary Camp (Dungeon)',
	'nmrb': 'Mercenary Camp (Underground)',
	'nmrc': 'Mercenary Camp (Sunken Ruins)',
	'nmrd': 'Mercenary Camp (Icecrown Glacier)',
	'nmre': 'Mercenary Camp (Outland)',
	'nmrf': 'Mercenary Camp (Black Citadel)',
	'ndrk': 'Black Dragon Roost',
	'ndru': 'Blue Dragon Roost',
	'ndrz': 'Bronze Dragon Roost',
	'ndrg': 'Green Dragon Roost',
	'ndro': 'Nether Dragon Roost',
	'ndrr': 'Red Dragon Roost',
	'nmrk': 'Marketplace',
	'nfoh': 'Fountain of Health',
	'nmoo': 'Fountain of Mana',
	'bDNR': 'Random Fountain',
	'nwgt': 'Way Gate'
};

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
/* relevant classes:
	.hp-toggle: master class
	.hp-highlight: give it cursor and link-style mouseover color
	.hp-control: this is a control button so never hide it
	.hp-display: this is the actual info display so don't give it an onclick to hide itself */
(() => {
	document.addEventListener("DOMContentLoaded", () => {
		document.querySelectorAll('.hp-toggle').forEach(el => {
			const { group } = el.dataset;
			const toggleClass = el.dataset.class || 'hidden';
			if (el.classList.contains('hp-display')) return;
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

/* Replay view navkeys (square brackets for prev/next) */
(() => {
	document.addEventListener("DOMContentLoaded", () => {
		var backElem = document.getElementById("prevReep");
		var forwardElem = document.getElementById("nextReep");
		document.onkeyup = function (e) {
			if (e.which == 219) {
				if (backElem) {
					window.location = backElem.href;
				}
			} else if (e.which == 221) {
				if (forwardElem) {
					window.location = forwardElem.href;
				}
			}
		};
	});
})();

/* Minimap drawings */
(() => {
	// Loads the image files even if they don't need to be drawn,
	// but on the other hand it starts loading and caching immediately.
	const startImg = new Image();
	startImg.src = '/static/images/drawmap_sloc.png';
	const goldImg = new Image();
	goldImg.src = '/static/images/drawmap_mine.png';
	const playImg = new Image();
	playImg.src = '/static/images/drawmap_play.png';

	const setupMap = (cnv, mapSize) => {
		mapImageSize = cnv.clientWidth;
		xSize = mapSize[1] - mapSize[0];
		ySize = mapSize[3] - mapSize[2];
		maxSize = Math.max(xSize, ySize);
		scale = mapImageSize / maxSize;
	}

	document.addEventListener("DOMContentLoaded", () => {
		document.body.querySelectorAll('.drawmap').forEach(async cnv => {
			const mapSize = JSON.parse(cnv.dataset.mapsize);
			const playerTowers = JSON.parse(cnv.dataset.towers || '{}');
			const playerStartLocations = JSON.parse(cnv.dataset.playerstarts || '{}');	// player starting locations for tower drawings
			const mapStartLocations = JSON.parse(cnv.dataset.mapstarts || '[]');		// generic starting locations for map details
			const goldMines = JSON.parse(cnv.dataset.mines || '[]');
			const neutralBuildings = JSON.parse(cnv.dataset.neutrals || '[]');
			const animated = cnv.classList.contains('anim');
			const delayed = cnv.classList.contains('delay');
			const detailed = (typeof cnv.dataset.neutrals !== 'undefined');
			const mapImg = delayed
				? cnv.parentNode.querySelector('img')
				: undefined;

			let images = {};

			neutralBuildings.forEach(b => {
				if (!(b[2] in images)) {
					img = new Image();
					img.src = '/static/images/game/neutrals/' + b[2] + '.png';
					images[b[2]] = img;
				}
			});

			// There's a race condition where it will draw transparent images
			// if they're not loaded before drawing
			const imagesReady = (mapImg = { complete: true, addEventListener: () => { } }) => {
				images['start'] = startImg;
				images['ngol'] = goldImg;
				images['play'] = playImg;
				images['map'] = mapImg;
				if (Object.values(images).every(i => i.complete)) return Promise.resolve();
				return new Promise(resolve => {
					Object.values(images).forEach(img => {
						img.addEventListener('error', resolve);
						img.addEventListener('load', () => {
							if (Object.values(images).every(i => i.complete)) resolve();
						});
					});
				});
			};

			// Tower and player start location size
			const ps = cnv.dataset.paintsize;
			const po = ps / 2;
			// Goldmine and map start location size
			const gs = ps * 3;
			const go = gs / 2;
			// Neutral size
			const ns = ps * 6;
			const no = ns / 2

			// Turn camera bounds into minimap bounds
			mapSize[0] -= 504;
			mapSize[1] += 504;
			mapSize[2] -= 248;
			mapSize[3] += 248;

			// Wait for map image to load and grow to real size when necessary
			if (delayed) await imagesReady(mapImg);

			setupMap(cnv, mapSize);

			const xStart = -(xSize / maxSize * mapImageSize - mapImageSize) / 2;
			const yStart = -(ySize / maxSize * mapImageSize - mapImageSize) / 2;

			const getCoords = t => ([
				Math.round((t[0] - mapSize[0]) * scale + xStart),
				Math.round(mapImageSize - ((t[1] - mapSize[2]) * scale + yStart))]);

			cnv.height = cnv.width = mapImageSize * 2;	// draw at triple resolution so the expanded image isn't upscaled and blurry
			const ctx = cnv.getContext('2d');
			ctx.scale(2, 2);

			const drawBase = () => {
				mapStartLocations.forEach(s => {
					const c = getCoords(s);
					ctx.drawImage(startImg, c[0] - go, c[1] - go, gs, gs);
					ctx.globalCompositeOperation = "source-atop";
					ctx.fillStyle = s[2];
					ctx.fillRect(c[0] - go, c[1] - go, gs, gs);
					ctx.globalCompositeOperation = "source-over";
				});
				goldMines.forEach(m => {
					const c = getCoords(m);
					ctx.drawImage(goldImg, c[0] - go, c[1] - go, gs, gs);
				});
				neutralBuildings.forEach(b => {
					const c = getCoords(b);
					ctx.drawImage(images[b[2]], c[0] - no, c[1] - no, ns, ns);
				});
				for (let [color, start] of Object.entries(playerStartLocations)) {
					ctx.fillStyle = color;
					const c = getCoords(start);
					ctx.fillRect(c[0] - ps, c[1] - ps, ps * 2, ps * 2);
				}
			}

			let mineRects = [];
			let neutralRects = [];

			const setupAreas = (scaleFactor) => {
				mineRects = [];
				goldMines.forEach(m => {
					const c = getCoords(m);
					let x1 = c[0] - go * scaleFactor;
					let y1 = c[1] - go * scaleFactor;
					let x2 = x1 + gs * scaleFactor;
					let y2 = y1 + gs * scaleFactor;
					mineRects.push([x1, y1, x2, y2, m[2]])
				});
				scaleFactor = scaleFactor * 0.8		// The neutralBuilding image size is a little too large
				neutralRects = [];
				neutralBuildings.forEach(b => {
					const c = getCoords(b);
					let x1 = c[0] - no * scaleFactor;
					let y1 = c[1] - no * scaleFactor;
					let x2 = x1 + ns * scaleFactor;
					let y2 = y1 + ns * scaleFactor;
					neutralRects.push([x1, y1, x2, y2, b[2]]);
				});
			}

			const isInRect = (click, rect) => (click[0] >= rect[0] && click[0] <= rect[2] && click[1] >= rect[1] && click[1] <= rect[3]);

			const handleMove = (e) => {
				offsetLeft = Math.round(cnv.getBoundingClientRect().left);
				offsetTop = Math.round(cnv.getBoundingClientRect().top);
				const mousePos = [e.clientX - offsetLeft, e.clientY - offsetTop];
				const maptip = document.getElementById('maptip');
				let tipVisible = 0;
				mineRects.forEach(r => {
					if (isInRect(mousePos, r)) {
						tipVisible = 1;
						tipText = `<b>${r[4]}</b> gold`;
					}
				})
				neutralRects.forEach(r => {
					if (isInRect(mousePos, r)) {
						tipVisible = 1;
						tipText = neutralBuildingCodes[r[4]]
					}
				})
				if (tipVisible === 1) {
					maptip.style.display = 'block';
					maptip.style.top = (mousePos[1]) + 'px';
					maptip.style.left = (mousePos[0] + 20) + 'px';
					maptip.childNodes[0].innerHTML = tipText;
				}
				if (tipVisible === 0) {
					maptip.style.display = 'none';
				}
			}

			cnv.addEventListener('mousemove', (e) => {
				if (detailed) {
					handleMove(e);
				}
			});

			// I think this is good enough for mobile...
			cnv.addEventListener('touchend', (e) => {
				if (detailed) {
					handleMove(e);
				}
			});

			// Enter bigmode
			cnv.addEventListener('click', () => {
				if (detailed) {
					let parent = event.target.parentNode;
					parent.classList.toggle('lesshuge');
					setupMap(cnv, mapSize);
					setupAreas(mapImageSize / 550);
				}
			});

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

			// If we don't redo the mouseover areas on window resize in bigmode they'll be bungled
			const handleResize = () => {
				setupMap(cnv, mapSize);
				setupAreas(mapImageSize / 550);
			}

			// Always wait for asset images to load before drawing them,
			// also wait for the map image to load when necessary
			if (animated || delayed) await imagesReady(mapImg);
			if (detailed) {
				window.addEventListener('resize', handleResize);
				setupAreas(1);
			}
			drawBase();
			if (animated) {
				// Animated minimap
				// ctx.fillStyle = '#000C';
				// ctx.fillRect((mapImageSize / 2) - 30, (mapImageSize / 2) - 30, 60, 60);
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


