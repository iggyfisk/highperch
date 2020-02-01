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
		const backElem = document.getElementById("prevReep");
		const forwardElem = document.getElementById("nextReep");
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

	let mapImageSize
		, xSize
		, ySize
		, maxSize
		, scale
		, xStart
		, yStart
		, currentZoom;

	const precisionRound = (number, precision) => {
		return Math.round(number * (10 ** (precision - 1))) / (10 ** (precision - 1))
	}

	const setupMap = (cnv, mapSize, initialSize) => {
		mapImageSize = cnv.clientWidth;
		xSize = mapSize[1] - mapSize[0];
		ySize = mapSize[3] - mapSize[2];
		maxSize = Math.max(xSize, ySize);
		scale = mapImageSize / maxSize;
		xStart = -(xSize / maxSize * mapImageSize - mapImageSize) / 2;
		yStart = -(ySize / maxSize * mapImageSize - mapImageSize) / 2;
		currentZoom = mapImageSize / initialSize;
	}

	const makeCreepTable = camp => {
		const creepTable = document.createElement("table");
		let totalExp = 0;
		camp['creeps'].forEach(creep => {
			const creepRow = creepTable.insertRow();
			creepRow.className = 'creeprow';
			const countCell = creepRow.insertCell();
			if (creep['count'] > 1) { countCell.append(document.createTextNode(creep['count'] + ' ⨯')); }
			countCell.className = 'count';
			const iconCell = creepRow.insertCell();
			const iconImg = new Image();
			iconImg.src = `/static/images/game/creeps/${creep['id']}.png`;
			iconCell.append(iconImg);
			iconCell.className = 'creepicon';
			const nameCell = creepRow.insertCell();
			nameCell.append(document.createTextNode(creepCodes[creep['id']]['name']));
			nameCell.className = 'creepname';
			const levelCell = creepRow.insertCell();
			levelCell.append(document.createTextNode(creepCodes[creep['id']]['level']));
			levelCell.className = 'level';
			const expCell = creepRow.insertCell();
			expCell.className = 'exp';
			const rowExp = levelExp[creepCodes[creep['id']]['level']] * creep['count'];
			totalExp += rowExp;
			expCell.append(document.createTextNode(rowExp));
			const dropCell = creepRow.insertCell();
			dropCell.className = 'drops';
			creep['drops'].forEach(drop => {
				const dropDiv = document.createElement("div");
				dropDiv.className = 'drop';
				if (Array.isArray(drop)) {
					if (drop.length > 0) {
						dropDiv.className += ' droptable';
						drop.forEach(item => {
							const itemImg = new Image();
							itemImg.src = `/static/images/game/items/${item}.png`;
							itemImg.title = itemCodes[item]['name'];
							dropDiv.appendChild(itemImg);
						})
					}
				} else {
					const itemImg = new Image();
					itemImg.src = `/static/images/game/items/${drop}.png`;
					itemImg.title = itemCodes[drop]['name'];
					dropDiv.appendChild(itemImg);
				}
				dropCell.appendChild(dropDiv);
			})
		});

		const totalRow = creepTable.insertRow();
		totalRow.className = 'total';
		let countCell = totalRow.insertCell();
		let iconCell = totalRow.insertCell();
		let nameCell = totalRow.insertCell();
		nameCell.append(document.createTextNode('total'));
		let levelCell = totalRow.insertCell();
		levelCell.append(document.createTextNode(camp['level']));
		let expCell = totalRow.insertCell();
		expCell.className = 'exp totalexp';
		expCell.append(document.createTextNode(totalExp));
		let dropCell = totalRow.insertCell();

		const tableCols = ['', '', '', 'level', 'exp', ''];
		const tableHeader = creepTable.createTHead();
		const tableHeadRow = tableHeader.insertRow();
		tableCols.forEach(col => {
			const th = document.createElement("th");
			th.appendChild(document.createTextNode(col));
			tableHeadRow.appendChild(th);
		});

		return creepTable;
	}

	document.addEventListener("DOMContentLoaded", () => {
		document.body.querySelectorAll('.drawmap').forEach(async cnv => {
			const mapSize = JSON.parse(cnv.dataset.mapsize);
			const playerTowers = JSON.parse(cnv.dataset.towers || '{}');
			const playerStartLocations = JSON.parse(cnv.dataset.playerstarts || '{}');	// player starting locations for tower drawings
			const mapStartLocations = JSON.parse(cnv.dataset.mapstarts || '[]');		// generic starting locations for map details
			const goldMines = JSON.parse(cnv.dataset.mines || '[]');
			const neutralBuildings = JSON.parse(cnv.dataset.neutrals || '[]');
			const creepCamps = JSON.parse(cnv.dataset.creepcamps || '[]');
			const critters = JSON.parse(cnv.dataset.critters || '[]');
			const animated = cnv.classList.contains('anim');
			const delayed = cnv.classList.contains('delay');
			const detailed = (typeof cnv.dataset.neutrals !== 'undefined');
			const mapImg = delayed
				? cnv.parentNode.querySelector('img')
				: undefined;

			let images = {};

			neutralBuildings.forEach(b => {
				if (!(b[2] in images)) {
					const img = new Image();
					img.src = '/static/images/game/neutrals/' + b[2] + '.png';
					images[b[2]] = img;
				}
			});

			critters.forEach(c => {
				if (!(c['id'] in images)) {
					const img = new Image();
					img.src = '/static/images/game/critters/' + c['id'] + '.png';
					images[c['id']] = img;
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
			// Critter icon size
			const crs = ps * 4.5
			const cro = crs / 2

			// Turn camera bounds into minimap bounds
			mapSize[0] -= 504;
			mapSize[1] += 504;
			mapSize[2] -= 248;
			mapSize[3] += 248;

			// Wait for map image to load and grow to real size when necessary
			if (delayed) await imagesReady(mapImg);

			const initialSize = cnv.clientWidth;
			setupMap(cnv, mapSize, initialSize);

			const upResFactor = 2.5;

			const getCoords = t => {
				return [precisionRound(((t[0] - mapSize[0]) * scale + xStart), 3) / currentZoom,
				precisionRound((mapImageSize - ((t[1] - mapSize[2]) * scale + yStart)), 3) / currentZoom];
			}

			cnv.height = cnv.width = mapImageSize * upResFactor;	// draw at double resolution so the expanded image isn't upscaled and blurry
			const ctx = cnv.getContext('2d');
			ctx.scale(upResFactor, upResFactor);

			const getDotSize = camp => {
				if (camp['level'] < 10) {
					dotSize = 6;
				}
				else if (camp['level'] >= 10 && camp['level'] < 20) {
					dotSize = 7;
				}
				else if (camp['level'] >= 20) {
					dotSize = 8;
				}
				return dotSize;
			}

			const getDotColor = camp => {
				if (camp['level'] < 10) {
					dotColor = 'rgba(55, 170, 34, 0.8)';
				}
				else if (camp['level'] >= 10 && camp['level'] < 20) {
					dotColor = 'rgba(255, 106, 0, 0.8)';
				}
				else if (camp['level'] >= 20) {
					dotColor = 'rgba(227, 0, 0, 0.7)';
				}
				return dotColor;
			}

			const drawCritters = () => {
				critters.forEach(critter => {
					const c = getCoords([critter['x'], critter['y']]);
					ctx.drawImage(images[critter['id']], c[0] - cro, c[1] - cro, crs / currentZoom, crs / currentZoom);
				});
			}

			const drawBase = () => {
				if (detailed) {
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

					creepCamps.forEach(camp => {
						c = getCoords([camp['x'], camp['y']])
						const radius = getDotSize(camp);
						const color = getDotColor(camp);
						ctx.beginPath();
						ctx.arc(c[0], c[1], radius, 0, 2 * Math.PI, false);
						ctx.fillStyle = color;
						ctx.fill();
						ctx.arc(c[0], c[1], radius, 0, 2 * Math.PI);
						const gradient = ctx.createRadialGradient(c[0], c[1], 0, c[0], c[1], radius);
						if (radius === 7) { gradient.addColorStop(0, 'rgba(100, 100, 100, 0.1)'); }	// orange dots need a different gradient
						else { gradient.addColorStop(0, 'rgba(50, 50, 50, 0.3)'); }
						gradient.addColorStop(1, color);
						ctx.fillStyle = gradient;
						ctx.fill();
						ctx.lineWidth = 1;
						ctx.strokeStyle = '#003300';
						ctx.stroke();
					})
				}

				for (let [color, start] of Object.entries(playerStartLocations)) {
					ctx.fillStyle = color;
					const c = getCoords(start);
					ctx.fillRect(c[0] - ps, c[1] - ps, ps * 2, ps * 2);
				}
			}

			let mineRects = [];
			let neutralRects = [];
			let creepRects = [];

			const setupAreas = (scaleFactor) => {
				mineRects = [];
				goldMines.forEach(m => {
					const c = getCoords(m);
					let x1 = c[0] * scaleFactor - go * scaleFactor;
					let y1 = c[1] * scaleFactor - go * scaleFactor;
					let x2 = x1 + gs * scaleFactor;
					let y2 = y1 + gs * scaleFactor;
					mineRects.push([x1, y1, x2, y2, m[2]])
				});
				creepRects = [];
				creepCamps.forEach(camp => {
					cs = getDotSize(camp) * 3	// dotSize is a radius, and we want it a bit bigger than the actual dot
					co = cs / 2
					const c = getCoords([camp['x'], camp['y']]);
					let x1 = c[0] * scaleFactor - co * scaleFactor;
					let y1 = c[1] * scaleFactor - co * scaleFactor;
					let x2 = x1 + cs * scaleFactor;
					let y2 = y1 + cs * scaleFactor;
					creepRects.push([x1, y1, x2, y2, camp])
				});
				neutralRectShrink = 0.8		// The neutralBuilding image size is a little too large
				neutralRects = [];
				neutralBuildings.forEach(b => {
					const c = getCoords(b);
					let x1 = c[0] * scaleFactor - no * scaleFactor * neutralRectShrink;
					let y1 = c[1] * scaleFactor - no * scaleFactor * neutralRectShrink;
					let x2 = x1 + ns * scaleFactor * neutralRectShrink;
					let y2 = y1 + ns * scaleFactor * neutralRectShrink;
					neutralRects.push([x1, y1, x2, y2, b[2]]);
				});
			}

			const isInRect = (click, rect) => (click[0] >= rect[0] && click[0] <= rect[2] && click[1] >= rect[1] && click[1] <= rect[3]);

			let camp = {}

			const handleMove = (e) => {
				offsetLeft = Math.round(cnv.getBoundingClientRect().left);
				offsetTop = Math.round(cnv.getBoundingClientRect().top);
				const mousePos = [e.clientX - offsetLeft, e.clientY - offsetTop];
				const neutralTip = document.getElementById('neutraltip');
				let neutralVisible = 0;
				neutralText = '';
				mineRects.forEach(r => {
					if (isInRect(mousePos, r)) {
						neutralVisible = 1;
						neutralText = `<b>${r[4]}</b> gold`;
					}
				})
				neutralRects.forEach(r => {
					if (isInRect(mousePos, r)) {
						neutralVisible = 1;
						neutralText = neutralBuildingCodes[r[4]]
					}
				})

				// Todo: highlight the creep camp dots on mouseover.
				// Since we're baking this all into one canvas, 
				// we'll probably need a separate canvas on top for this

				if (neutralVisible === 1) {
					neutralTip.style.top = (mousePos[1] - 50) + 'px';
					neutralTip.style.left = (mousePos[0] - (neutralText.length ** 1.1 * 3)) + 'px';
					neutralTip.childNodes[0].innerHTML = neutralText;
					neutralTip.style.display = 'block';
				} else {
					neutralTip.style.display = 'none';
				}
			}

			if (detailed) {
				let campVisible = 0;
				let crittersVisible = 0;

				document.querySelectorAll('.mapzoom').forEach(zoomControl => {
					zoomControl.addEventListener('click', event => {
						event.target.classList.toggle('zoomenabled');
						mapImg.parentNode.classList.toggle('lesshuge');
						const campTip = document.getElementById('creeptip');
						campTip.style.display = 'none';
						campVisible = 0;
						setupMap(cnv, mapSize, initialSize);
						setupAreas(currentZoom);
						ctx.clearRect(0, 0, cnv.width, cnv.height);
						drawBase();
						if (crittersVisible === 1) {
							drawCritters();
						}
					});
				});

				document.querySelectorAll('.drawcritters').forEach(zoomControl => {
					zoomControl.addEventListener('click', event => {
						event.target.classList.toggle('crittersenabled');
						if (crittersVisible === 0) {
							drawCritters();
							crittersVisible = 1;
						}
						else {
							ctx.clearRect(0, 0, cnv.width, cnv.height);
							drawBase();
							crittersVisible = 0;
						}
					});
				});

				cnv.addEventListener('click', (e) => {
					offsetLeft = Math.round(cnv.getBoundingClientRect().left);
					offsetTop = Math.round(cnv.getBoundingClientRect().top);
					const mousePos = [e.clientX - offsetLeft, e.clientY - offsetTop];
					const campTip = document.getElementById('creeptip');

					let creepClicked = 0;

					creepRects.forEach(r => {
						if (isInRect(mousePos, r)) {
							creepClicked = 1;
							if (campVisible === 1 && r[4] === camp) {
								campTip.style.display = 'none';
								campVisible = 0;
							} else {
								campTip.innerHTML = '';
								camp = r[4];
								campVisible = 1;
								creepList = camp['creeps'];
								creepList.sort((a, b) => (creepCodes[b['id']]['level'] - creepCodes[a['id']]['level']))
								const creepDiv = makeCreepTable(camp);
								campTip.append(creepDiv);
								campTip.style.top = (mousePos[1]) + 'px';
								campTip.style.left = (mousePos[0] + 20) + 'px';
								campTip.style.display = 'inline';
								campVisible = 1;
							}
						}
					})
					if (creepClicked === 0) {
						campTip.style.display = 'none';
					}
				});

				cnv.addEventListener('mousemove', (e) => {
					handleMove(e);
				});

				// I think this is good enough for mobile...
				cnv.addEventListener('touchend', (e) => {
					handleMove(e);
				});
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

			// If we don't redo the mouseover areas on window resize in bigmode they'll be bungled
			const handleResize = () => {
				setupMap(cnv, mapSize, initialSize);
				setupAreas(currentZoom);
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
