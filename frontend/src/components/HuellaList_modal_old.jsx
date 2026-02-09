// Programa: Weblla
// Veersion: 1.0
// Autor: Equipo Weblla
// Fecha: 28-01-2026
// Descripción:
// Componente React para listar y buscar huellas con filtros, paginación y exportación CSV.
// Utiliza Axios para las solicitudes HTTP y maneja estados de carga y errores.

import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api/huellas/`
  : "/api/huellas/";

export default function HuellaList({ token }) {
  const [huellas, setHuellas] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState("");
  const [codigopostal, setCodigopostal] = useState("");
  const [provincia, setProvincia] = useState("");
  const [poblacion, setPoblacion] = useState("");
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(50);
  const [count, setCount] = useState(0);

  useEffect(() => {
    fetchHuellas();
  }, [page, pageSize]);

  async function fetchHuellas() {
    setLoading(true);
    setError(null);
    try {
      const params = {
        page: page,
        page_size: pageSize,
      };
      if (search) params.search = search;
      if (codigopostal) params.codigopostal = codigopostal;
      if (provincia) params.provincia = provincia;
      if (poblacion) params.poblacion = poblacion;

      const headers = {};
      if (token) {
        headers["Authorization"] = `Token ${token}`;
      }

      const resp = await axios.get(API_URL, { params, headers });
      const data = resp.data;
      const results = Array.isArray(data) ? data : data.results || [];
      setHuellas(results);
      setCount(data.count || results.length);
    } catch (e) {
      setError("Error cargando huellas: " + (e.message || e));
      setHuellas([]);
    } finally {
      setLoading(false);
    }
  }

  function handleSearchSubmit(e) {
    e.preventDefault();
    setPage(1);
    fetchHuellas();
  }

  function clearFilters() {
    setSearch("");
    setCodigopostal("");
    setProvincia("");
    setPoblacion("");
    setPage(1);
    fetchHuellas();
  }

  async function handleExportarCSV() {
    try {
      const params = new URLSearchParams();
      if (codigopostal) params.append("codigopostal", codigopostal);
      if (provincia) params.append("provincia", provincia);
      if (poblacion) params.append("poblacion", poblacion);

      const headers = {};
      if (token) {
        headers["Authorization"] = `Token ${token}`;
      }

      const exportUrl =
        `${import.meta.env.VITE_API_URL || ""}/api/huellas/exportar_csv/` +
        (params.toString() ? "?" + params.toString() : "");

      const response = await axios.get(exportUrl, {
        headers,
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "huellas.csv");
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (error) {
      alert("Error al exportar: " + error.message);
    }
  }

  return (
    <div>
      <h2>Búsqueda de Huellas</h2>

      {error && <div className="error">{error}</div>}

      <form className="filters" onSubmit={handleSearchSubmit}>
        <input
          placeholder="Buscar (texto libre)"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <input
          placeholder="Código postal"
          value={codigopostal}
          onChange={(e) => setCodigopostal(e.target.value)}
        />
        <input
          placeholder="Provincia"
          value={provincia}
          onChange={(e) => setProvincia(e.target.value)}
        />
        <input
          placeholder="Población"
          value={poblacion}
          onChange={(e) => setPoblacion(e.target.value)}
        />
        <button type="submit" className="btn">
          Buscar
        </button>
        <button
          type="button"
          onClick={clearFilters}
          className="btn btn-secondary"
        >
          Limpiar
        </button>
        <button
          type="button"
          onClick={handleExportarCSV}
          className="btn btn-success"
        >
          Exportar CSV
        </button>
      </form>

      {loading && <div className="info">Cargando...</div>}
      {!loading && huellas.length === 0 && !error && (
        <div className="info">No hay resultados.</div>
      )}

      {!loading && huellas.length > 0 && (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>CP</th>
                <th>Provincia</th>
                <th>Población</th>
                <th>Vía</th>
                <th>Número</th>
                <th>OLT</th>
                <th>CTO</th>
              </tr>
            </thead>
            <tbody>
              {huellas.map((h) => (
                <tr key={h.id}>
                  <td>{h.iddomicilioto}</td>
                  <td>{h.codigopostal}</td>
                  <td>{h.provincia}</td>
                  <td>{h.poblacion}</td>
                  <td>
                    {h.tipovia} {h.nombrevia}
                  </td>
                  <td>{h.numero}</td>
                  <td>{h.codigoolt}</td>
                  <td>{h.codigocto}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="controls">
        <div>
          <label>
            Resultados por página:
            <select
              value={pageSize}
              onChange={(e) => {
                setPageSize(Number(e.target.value));
                setPage(1);
              }}
              style={{ marginLeft: "8px" }}
            >
              <option value={10}>10</option>
              <option value={25}>25</option>
              <option value={50}>50</option>
              <option value={100}>100</option>
            </select>
          </label>
        </div>

        <div className="pagination">
          <button
            disabled={page <= 1}
            onClick={() => setPage((p) => Math.max(1, p - 1))}
          >
            Anterior
          </button>
          <span>Página {page}</span>
          <button
            disabled={huellas.length < pageSize}
            onClick={() => setPage((p) => p + 1)}
          >
            Siguiente
          </button>
        </div>
      </div>

      {count > 0 && <div className="footer-info">Total: {count} registros</div>}
    </div>
  );
}
