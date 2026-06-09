const API_BASE = "https://pokeapi.co/api/v2/pokemon";
const POKEMON_COUNT = 50;

// Grab the elements that only exist on one page or the other.
// This lets a single script.js file drive both index.html and details.html.
const grid = document.getElementById("pokemon-grid");
const detailsContainer = document.getElementById("pokemon-details");
const status = document.getElementById("status");

if (grid) {
  loadPokemonList();
}

if (detailsContainer) {
  loadPokemonDetails();
}

// ---- Index page: fetch the list and render cards in a CSS grid ----
async function loadPokemonList() {
  try {
    const listResponse = await fetch(`${API_BASE}?limit=${POKEMON_COUNT}`);
    const listData = await listResponse.json();

    // listData.results only gives us a name + url, so we await a second
    // fetch per Pokémon to get its image (sprite) and id.
    const pokemonDetails = await Promise.all(
      listData.results.map(async (pokemon) => {
        const response = await fetch(pokemon.url);
        return response.json();
      })
    );

    status.remove();
    pokemonDetails.forEach(renderCard);
  } catch (error) {
    status.textContent = "Something went wrong while loading Pokémon. Please try again later.";
    console.error(error);
  }
}

function renderCard(pokemon) {
  const card = document.createElement("article");
  card.className = "card";

  const image = document.createElement("img");
  image.src = pokemon.sprites.front_default;
  image.alt = pokemon.name;

  const name = document.createElement("h2");
  name.textContent = pokemon.name;

  const button = document.createElement("button");
  button.textContent = "View Details";
  // Pass the Pokémon's name as a query parameter so details.html knows which one to fetch.
  button.addEventListener("click", () => {
    window.location.href = `details.html?name=${pokemon.name}`;
  });

  card.append(image, name, button);
  grid.append(card);
}

// ---- Details page: read the query parameter and fetch that one Pokémon ----
async function loadPokemonDetails() {
  const params = new URLSearchParams(window.location.search);
  const name = params.get("name");

  if (!name) {
    status.textContent = "No Pokémon was selected. Go back and choose one from the list.";
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/${name}`);
    if (!response.ok) {
      throw new Error(`Pokémon "${name}" not found`);
    }
    const pokemon = await response.json();

    status.remove();
    renderDetails(pokemon);
  } catch (error) {
    status.textContent = "Could not load details for this Pokémon.";
    console.error(error);
  }
}

function renderDetails(pokemon) {
  const image = document.createElement("img");
  image.src = pokemon.sprites.front_default;
  image.alt = pokemon.name;

  const name = document.createElement("h2");
  name.textContent = `#${pokemon.id} ${pokemon.name}`;

  const types = document.createElement("p");
  types.className = "types";
  pokemon.types.forEach((typeInfo) => {
    const typeBadge = document.createElement("span");
    typeBadge.textContent = typeInfo.type.name;
    types.append(typeBadge);
  });

  const table = document.createElement("table");
  const rows = [
    ["Height", `${pokemon.height / 10} m`],
    ["Weight", `${pokemon.weight / 10} kg`],
    ["Abilities", pokemon.abilities.map((a) => a.ability.name).join(", ")],
    ["Base experience", pokemon.base_experience],
  ];

  rows.forEach(([label, value]) => {
    const row = document.createElement("tr");
    const labelCell = document.createElement("td");
    const valueCell = document.createElement("td");
    labelCell.textContent = label;
    valueCell.textContent = value;
    row.append(labelCell, valueCell);
    table.append(row);
  });

  detailsContainer.append(image, name, types, table);
}
