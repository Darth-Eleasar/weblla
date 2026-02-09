// Programa: Weblla
// Veersion: 1.0
// Autor: Equipo Weblla
// Fecha: 28-01-2026
// Descripción:
// Componente React para listar, buscar, filtrar, paginar, crear, editar y eliminar huellas.
// Incluye exportación a CSV y gestión de permisos basada en roles de usuario.

import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api/huellas/`
  : "/api/huellas/";

export default function HuellaList({ token, usuario }) {
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

  // Modal
  const [modalAbierto, setModalAbierto] = useState(false);
  const [huellaSeleccionada, setHuellaSeleccionada] = useState(null);
  const [huellaEditando, setHuellaEditando] = useState(null);
  const [guardandoModal, setGuardandoModal] = useState(false);
  const [nuevaHuella, setNuevaHuella] = useState(false);

  // Determinar permisos basados en roles
  const tienePermiso = (accion) => {
    if (!usuario || !usuario.grupos) return false;

    const rol = usuario.grupos[0]; // Primer rol del usuario

    if (rol === "Admin") return true; // Admin puede todo
    if (accion === "ver")
      return ["Admin", "Ingeniería", "Técnico"].includes(rol);
    if (accion === "editar") return ["Admin", "Ingeniería"].includes(rol);
    if (accion === "eliminar") return rol === "Admin";
    if (accion === "crear") return rol === "Admin";

    return false;
  };

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

  // Abrir modal con detalles de huella
  const abrirModalDetalle = (huella) => {
    setHuellaSeleccionada(huella);
    setHuellaEditando({ ...huella });
    setNuevaHuella(false);
    setModalAbierto(true);
  };

  // Abrir modal para crear nueva huella
  const abrirModalNueva = () => {
    setHuellaSeleccionada(null);
    setHuellaEditando({
      codigopostal: "",
      provincia: "",
      poblacion: "",
      nombrevia: "",
      numero: "",
      codigoolt: "",
      codigocto: "",
      // Agregar más campos según sea necesario
    });
    setNuevaHuella(true);
    setModalAbierto(true);
  };

  // Cerrar modal
  const cerrarModal = () => {
    setModalAbierto(false);
    setHuellaSeleccionada(null);
    setHuellaEditando(null);
    setNuevaHuella(false);
  };

  // Guardar cambios (crear o actualizar)
  const guardarHuella = async () => {
    setGuardandoModal(true);
    try {
      const headers = {};
      if (token) {
        headers["Authorization"] = `Token ${token}`;
      }

      let response;
      if (nuevaHuella) {
        // Crear nueva
        response = await axios.post(API_URL, huellaEditando, { headers });
      } else {
        // Actualizar existente
        const urlActualizar = `${API_URL}${huellaSeleccionada.id}/`;
        response = await axios.put(urlActualizar, huellaEditando, { headers });
      }

      // Cerrar modal y recargar datos
      cerrarModal();
      fetchHuellas();
      setError(null);
    } catch (err) {
      setError(
        "Error guardando huella: " +
          (err.response?.data?.detail || err.message),
      );
    } finally {
      setGuardandoModal(false);
    }
  };

  // Eliminar huella
  const eliminarHuella = async (id) => {
    if (!window.confirm("¿Está seguro que desea eliminar este registro?")) {
      return;
    }

    try {
      const headers = {};
      if (token) {
        headers["Authorization"] = `Token ${token}`;
      }

      const urlEliminar = `${API_URL}${id}/`;
      await axios.delete(urlEliminar, { headers });

      cerrarModal();
      fetchHuellas();
      setError(null);
    } catch (err) {
      setError(
        "Error eliminando huella: " +
          (err.response?.data?.detail || err.message),
      );
    }
  };

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
        {tienePermiso("crear") && (
          <button
            type="button"
            onClick={abrirModalNueva}
            className="btn btn-success"
          >
            Nuevo
          </button>
        )}
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
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {huellas.map((h) => (
                <tr
                  key={h.id}
                  style={{
                    cursor: tienePermiso("ver") ? "pointer" : "default",
                  }}
                  onClick={() => tienePermiso("ver") && abrirModalDetalle(h)}
                >
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
                  <td onClick={(e) => e.stopPropagation()}>
                    {tienePermiso("editar") && (
                      <button
                        onClick={() => abrirModalDetalle(h)}
                        className="btn btn-small"
                      >
                        Editar
                      </button>
                    )}
                    {tienePermiso("eliminar") && (
                      <button
                        onClick={() => eliminarHuella(h.id)}
                        className="btn btn-small btn-danger"
                      >
                        Eliminar
                      </button>
                    )}
                  </td>
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

      {/* MODAL */}
      {modalAbierto && (
        <div
          className="modal-overlay"
          onClick={cerrarModal}
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: "rgba(0,0,0,0.5)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            zIndex: 1000,
          }}
        >
          <div
            className="modal-content"
            onClick={(e) => e.stopPropagation()}
            style={{
              backgroundColor: "white",
              borderRadius: "4px",
              border: "1px solid #ddd",
              width: "90%",
              maxWidth: "700px",
              maxHeight: "90vh",
              overflow: "auto",
              boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
            }}
          >
            <div
              style={{
                padding: "20px",
                borderBottom: "1px solid #ddd",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <h3 style={{ margin: 0 }}>
                {nuevaHuella ? "Nueva Huella" : "Detalles de Huella"}
              </h3>
              <button
                onClick={cerrarModal}
                style={{
                  background: "none",
                  border: "none",
                  fontSize: "20px",
                  cursor: "pointer",
                  color: "#666",
                }}
              >
                ✕
              </button>
            </div>

            <div style={{ padding: "20px" }}>
              {/* Grid de campos */}
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: "15px",
                }}
              >
                {Object.keys(huellaEditando || {}).map((campo) => (
                  <div key={campo} className="form-group">
                    <label style={{ textTransform: "capitalize" }}>
                      {campo.replace(/_/g, " ")}
                    </label>
                    <input
                      type="text"
                      value={huellaEditando[campo] || ""}
                      onChange={(e) =>
                        setHuellaEditando({
                          ...huellaEditando,
                          [campo]: e.target.value,
                        })
                      }
                      disabled={!tienePermiso("editar")}
                      style={{
                        backgroundColor: tienePermiso("editar")
                          ? "white"
                          : "#f5f5f5",
                      }}
                    />
                  </div>
                ))}
              </div>

              {/* Botones de acción */}
              <div
                style={{
                  marginTop: "20px",
                  display: "flex",
                  gap: "10px",
                  justifyContent: "flex-end",
                }}
              >
                <button onClick={cerrarModal} className="btn btn-secondary">
                  Cerrar
                </button>

                {tienePermiso("editar") && (
                  <button
                    onClick={guardarHuella}
                    disabled={guardandoModal}
                    className="btn btn-success"
                  >
                    {guardandoModal ? "Guardando..." : "Guardar"}
                  </button>
                )}

                {!nuevaHuella && tienePermiso("eliminar") && (
                  <button
                    onClick={() => eliminarHuella(huellaSeleccionada.id)}
                    className="btn btn-danger"
                  >
                    Eliminar
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
