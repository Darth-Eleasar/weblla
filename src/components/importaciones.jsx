// Programa: Weblla
// Veersion: 1.0
// Autor: Equipo Weblla
// Fecha: 28-01-2026
// Descripción:
// Componente React para la gestión de importaciones de archivos CSV.
// Permite a los usuarios con los permisos adecuados subir archivos,
// ver el historial de importaciones y procesar los archivos subidos.
// Los permisos se basan en los roles de usuario: Admin, Ingeniería y Técnico.
// Utiliza Axios para las solicitudes HTTP a la API backend.

import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function Importaciones({ token, usuario }) {
  const [file, setFile] = useState(null);
  const [importaciones, setImportaciones] = useState([]);
  const [loading, setLoading] = useState(false);
  const [mensaje, setMensaje] = useState("");

  // Determinar permisos basados en roles
  const tienePermiso = (accion) => {
    if (!usuario || !usuario.grupos) return false;

    const rol = usuario.grupos[0];

    if (rol === "Admin") return true;
    if (accion === "ver")
      return ["Admin", "Ingeniería", "Técnico"].includes(rol);
    if (accion === "procesar") return ["Admin", "Ingeniería"].includes(rol);
    if (accion === "subir") return ["Admin", "Ingeniería"].includes(rol);

    return false;
  };

  useEffect(() => {
    fetchImportaciones();
  }, []);

  const fetchImportaciones = async () => {
    try {
      const headers = {};
      if (token) {
        headers["Authorization"] = `Token ${token}`;
      }
      const res = await axios.get(`${API_URL}/api/importaciones/`, { headers });
      setImportaciones(res.data.results || res.data);
    } catch (error) {
      console.error("Error cargando lista:", error);
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMensaje("");
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setMensaje("Selecciona un archivo primero");
      return;
    }

    const formData = new FormData();
    formData.append("fichero_original", file);

    setLoading(true);
    try {
      const headers = {};
      if (token) {
        headers["Authorization"] = `Token ${token}`;
      }

      await axios.post(`${API_URL}/api/importaciones/`, formData, {
        headers,
      });
      setMensaje("Archivo subido correctamente");
      setFile(null);
      document.getElementById("fileInput").value = "";
      fetchImportaciones();
    } catch (error) {
      setMensaje(
        "Error al subir: " + (error.response?.data?.detail || error.message),
      );
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleProcess = async (id) => {
    try {
      setLoading(true);
      const headers = {};
      if (token) {
        headers["Authorization"] = `Token ${token}`;
      }
      await axios.post(
        `${API_URL}/api/importaciones/${id}/procesar/`,
        {},
        {
          headers,
        },
      );
      setMensaje(`Importación ${id} procesada`);
      fetchImportaciones();
    } catch (error) {
      setMensaje(
        "Error al procesar: " + (error.response?.data?.detail || error.message),
      );
    } finally {
      setLoading(false);
    }
  };

  // No mostrar nada si el usuario no tiene permisos de lectura
  if (!tienePermiso("ver")) {
    return (
      <div className="error">
        No tiene permisos para acceder a esta sección.
      </div>
    );
  }

  return (
    <div>
      <h2>Importar CSV</h2>

      {mensaje && (
        <div className={mensaje.includes("Error") ? "error" : "success"}>
          {mensaje}
        </div>
      )}

      {tienePermiso("subir") && (
        <div className="filters">
          <form
            onSubmit={handleUpload}
            style={{
              display: "flex",
              gap: "10px",
              alignItems: "center",
              flex: 1,
            }}
          >
            <input
              id="fileInput"
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              style={{ flex: 1 }}
            />
            <button type="submit" disabled={loading || !file} className="btn">
              {loading ? "Subiendo..." : "Subir Archivo"}
            </button>
          </form>
        </div>
      )}

      {!tienePermiso("subir") && (
        <div className="info">
          No tiene permisos para subir archivos. Solo Admin e Ingeniería pueden
          importar CSV.
        </div>
      )}

      <h3 style={{ marginTop: "30px", marginBottom: "15px" }}>
        Histórico de Cargas
      </h3>

      {importaciones.length === 0 ? (
        <div className="info">No hay importaciones aún.</div>
      ) : (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Fecha</th>
                <th>Usuario</th>
                <th>Archivo</th>
                <th>Estado</th>
                <th>Acciones</th>
                <th>Log</th>
              </tr>
            </thead>
            <tbody>
              {importaciones.map((imp) => (
                <tr key={imp.id}>
                  <td>{imp.id}</td>
                  <td>{new Date(imp.fecha_creacion).toLocaleString()}</td>
                  <td>{imp.usuario_nombre || imp.usuario}</td>
                  <td>
                    <a
                      href={imp.fichero_original}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Descargar
                    </a>
                  </td>
                  <td>
                    <span
                      style={{
                        padding: "3px 8px",
                        borderRadius: "3px",
                        backgroundColor:
                          imp.estado === "ERROR"
                            ? "#fce4e4"
                            : imp.estado === "COMPLETADO"
                              ? "#eafce4"
                              : "#e8f4f8",
                        color:
                          imp.estado === "ERROR"
                            ? "#ba2121"
                            : imp.estado === "COMPLETADO"
                              ? "#28a745"
                              : "#0c4a78",
                        fontSize: "11px",
                        fontWeight: 600,
                      }}
                    >
                      {imp.estado}
                    </span>
                  </td>
                  <td>
                    {imp.estado === "PENDIENTE" && tienePermiso("procesar") && (
                      <button
                        onClick={() => handleProcess(imp.id)}
                        disabled={loading}
                        className="btn btn-small"
                      >
                        Procesar
                      </button>
                    )}
                    {imp.estado === "PENDIENTE" &&
                      !tienePermiso("procesar") && (
                        <span style={{ color: "#999", fontSize: "11px" }}>
                          Pendiente
                        </span>
                      )}
                    {imp.estado === "COMPLETADO" && (
                      <span style={{ color: "#28a745", fontSize: "11px" }}>
                        Completado
                      </span>
                    )}
                    {imp.estado === "ERROR" && (
                      <span style={{ color: "#ba2121", fontSize: "11px" }}>
                        Error
                      </span>
                    )}
                  </td>
                  <td style={{ fontSize: "11px", color: "#666" }}>
                    {imp.log_proceso
                      ? imp.log_proceso.substring(0, 50) + "..."
                      : "-"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
