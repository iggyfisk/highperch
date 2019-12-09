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


/* Towers/TPM visibility toggle */
(() => {
	document.addEventListener("DOMContentLoaded", () => {
		const towerSpans = document.querySelectorAll('.towerdata');
		const tpmSpans = document.querySelectorAll('.tpmdata');
		towerSpans.forEach(item => {
			item.addEventListener('click', event => {
				towerSpans.forEach(ts => {
					ts.style.display = 'none';
				})
				tpmSpans.forEach(ts => {
					ts.style.display = 'inline';
				})
			});
		});
		tpmSpans.forEach(item => {
			item.addEventListener('click', event => {
				tpmSpans.forEach(ts => {
					ts.style.display = 'none';
				})
				towerSpans.forEach(ts => {
					ts.style.display = 'inline';
				})
			});
		});
	});
})();

/* Actions/APM visibility toggle */
/* Todo: generalize this with the other toggles using parent node stuff */
(() => {
	document.addEventListener("DOMContentLoaded", () => {
		const actionSpans = document.querySelectorAll('.actiondata');
		const apmSpans = document.querySelectorAll('.apmdata');
		actionSpans.forEach(item => {
			item.addEventListener('click', event => {
				actionSpans.forEach(as => {
					as.style.display = 'none';
				})
				apmSpans.forEach(as => {
					as.style.display = 'inline';
				})
			});
		});
		apmSpans.forEach(item => {
			item.addEventListener('click', event => {
				apmSpans.forEach(as => {
					as.style.display = 'none';
				})
				actionSpans.forEach(as => {
					as.style.display = 'inline';
				})
			});
		});
	});
})();

/* Detailed feedstats visibility toggle */
/* Todo: generalize this with the other toggles using parent node stuff */
(() => {
	document.addEventListener("DOMContentLoaded", () => {
		const feedSummarySpans = document.querySelectorAll('.feedsummary');
		const feedDetailSpans = document.querySelectorAll('.feeddetails');
		feedSummarySpans.forEach(item => {
			item.addEventListener('click', event => {
				feedSummarySpans.forEach(fs => {
					fs.style.display = 'none';
				})
				feedDetailSpans.forEach(fs => {
					fs.style.display = 'inline';
				})
			});
		});
		feedDetailSpans.forEach(item => {
			item.addEventListener('click', event => {
				feedDetailSpans.forEach(fs => {
					fs.style.display = 'none';
				})
				feedSummarySpans.forEach(fs => {
					fs.style.display = 'inline';
				})
			});
		});
	});
})();


/* Minimap drawings */
(() => {
	document.addEventListener("DOMContentLoaded", () => {
		document.body.querySelectorAll('.drawmap').forEach(cnv => {
			const playerTowers = JSON.parse(cnv.dataset.towers);
			const playerLocations = JSON.parse(cnv.dataset.startlocations);
			const mapSize = JSON.parse(cnv.dataset.mapsize);
			const ps = cnv.dataset.paintsize;
			const po = ps / 2;

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

			const drawStarts = () => {
				for (let [color, start] of Object.entries(playerLocations)) {
					ctx.fillStyle = color;
					const c = getCoords(start);
					ctx.fillRect(c[0] - ps, c[1] - ps, ps * 2, ps * 2);
				}
			}

			let queue = false;
			const animate = towers => {
				if (queue) return;
				queue = true;

				cnv.classList.toggle('anim');
				ctx.clearRect(0, 0, cnv.width, cnv.height);
				drawStarts();

				// Fixed delay between each paint, but adjusted per replay, 15 - 250ms;
				const frameDelay = Math.round(Math.max(Math.min(10000 / towers.length, 250), 15));
				const drawNext = (i) => {
					ctx.fillStyle = towers[i][3];
					coords = getCoords(towers[i++]);
					ctx.fillRect(coords[0] - po, coords[1] - po, ps, ps);

					if (i < towers.length) {
						setTimeout(drawNext.bind(this, i), frameDelay);
					} else {
						queue = false;
						cnv.classList.toggle('anim');
					}
				}
				setTimeout(drawNext.bind(this, 0), 1);
			}

			drawStarts();
			if (cnv.classList.contains('anim')) {
				// Will have to bite the bullet and add something to the DOM instead
				ctx.font = "40px sans";
				ctx.fillText("▶️", (mapImageSize / 2) - 25, (mapImageSize / 2) + 15);

				// Combine all players' towers and put them in order
				const orderedTowers = Object.entries(playerTowers)
					.map(([c, towers]) => towers.map(t => [...t, c]))
					.flat(1).sort((a, b) => (a[2] - b[2]));

				cnv.addEventListener('click', () => animate(orderedTowers));
			} else {
				for (let [color, towers] of Object.entries(playerTowers)) {
					ctx.fillStyle = color;
					towers.map(getCoords).forEach(c => { ctx.fillRect(c[0] - po, c[1] - po, ps, ps) });
				}
			}
		});
	});
})();


