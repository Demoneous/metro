<script>
  import { onMount } from 'svelte';

  let ports = [];
  let filteredPorts = [];
  let loading = true;
  let error = '';
  let searchQuery = '';
  let sortColumn = '';
  let sortAsc = true;

  async function fetchPorts() {
    loading = true;
    error = '';
    try {
      const response = await fetch('http://10.39.5.189:5000/ports');
      if (!response.ok) throw new Error(`Server error: ${response.status}`);
      ports = await response.json();
      filteredPorts = [...ports];
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  }

  function handleSearch() {
    const query = searchQuery.toLowerCase();
    filteredPorts = ports.filter(p =>
      p.port_id.toLowerCase().includes(query) || p.description.toLowerCase().includes(query)
    );
  }

  function sortBy(column) {
    if (sortColumn === column) {
      sortAsc = !sortAsc;
    } else {
      sortColumn = column;
      sortAsc = true;
    }

    filteredPorts.sort((a, b) => {
      const valA = a[column].toLowerCase();
      const valB = b[column].toLowerCase();
      if (valA < valB) return sortAsc ? -1 : 1;
      if (valA > valB) return sortAsc ? 1 : -1;
      return 0;
    });
  }

  onMount(() => {
    fetchPorts();
  });
</script>

<style>
:global(body) {
  background-color: #121212;
  color: #fff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1 {
  margin-bottom: 1rem;
}

input {
  padding: 0.5rem 1rem;
  border: 1px solid #444;
  border-radius: 6px;
  background-color: #1e1e1e;
  color: #fff;
  width: 100%;
  max-width: 400px;
  margin-bottom: 1rem;
}

.table-container {
  overflow-x: auto;
  border-radius: 10px;
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.05);
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: #1e1e1e;
}

th, td {
  padding: 12px 16px;
  border-bottom: 1px solid #333;
  text-align: left;
}

thead {
  background-color: #2c2c2c;
  cursor: pointer;
}

th.sort-asc::after {
  content: " ▲";
}

th.sort-desc::after {
  content: " ▼";
}

tbody tr:nth-child(even) {
  background-color: #2a2a2a;
}

tbody tr:hover {
  background-color: #333;
  transition: background-color 0.2s ease-in-out;
}
</style>

<h1>Daftar Port</h1>

<input
  type="text"
  bind:value={searchQuery}
  placeholder="Cari port ID atau deskripsi..."
  on:input={handleSearch}
/>

{#if loading}
  <p>Memuat data port...</p>
{:else if error}
  <p class="error">Terjadi kesalahan: {error}</p>
{:else if filteredPorts.length === 0}
  <p>Tidak ada data port tersedia.</p>
{:else}
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th on:click={() => sortBy('port_id')}
              class:sort-asc={sortColumn === 'port_id' && sortAsc}
              class:sort-desc={sortColumn === 'port_id' && !sortAsc}>
            Port ID
          </th>
          <th on:click={() => sortBy('description')}
              class:sort-asc={sortColumn === 'description' && sortAsc}
              class:sort-desc={sortColumn === 'description' && !sortAsc}>
            Deskripsi
          </th>
        </tr>
      </thead>
      <tbody>
        {#each filteredPorts as port}
          <tr>
            <td>{port.port_id}</td>
            <td>{port.description}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
{/if}
