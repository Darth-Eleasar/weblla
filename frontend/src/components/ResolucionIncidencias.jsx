// Programa: Weblla
// Veersion: 1.0
// Autor: Equipo Weblla
// Fecha: 28-01-2026
// Descripción:
// Componente React para la resolución de incidencias en importaciones de datos.
// Permite a los usuarios ver, corregir y guardar incidencias detectadas durante la importación.
// Utiliza Axios para las solicitudes HTTP y maneja el estado con hooks de React.

import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function ResolucionIncidencias({ importacionId, token }) {
  const [importacion, setImportacion] = useState(null);
  const [incidencias, setIncidencias] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [editando, setEditando] = useState({});
  const [guardando, setGuardando] = useState(false);

  useEffect(() => {
    cargarIncidencias();
  }, [importacionId]);

  const cargarIncidencias = async () => {
    setLoading(true);
    try {
      const headers = {};
      if (token) headers["Authorization"] = `Token ${token}`;

      const resp = await axios.get(
        `${API_URL}/api/importaciones/${importacionId}/`,
        { headers },
      );
      setImportacion(resp.data);

      if (resp.data.fichero_errores) {
        const fileResp = await axios.get(resp.data.fichero_errores, {
          headers,
        });
        const lineas = fileResp.data.split("\n").filter((l) => l.trim());
        const datos = lineas.map((l) => {
          const partes = l.split("|");
          return {
            numLinea: partes[0],
            original: partes[1],
            error: partes[2],
            sugerencias: partes[3] ? partes[3].split(",") : [],
            correccion: partes[4] || "",
          };
        });
        setIncidencias(datos);
      }
    } catch (err) {
      setError("Error cargando incidencias: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const actualizarIncidencia = (index, nuevaCorreccion) => {
    const nuevoEditando = { ...editando };
    nuevoEditando[index] = nuevaCorreccion;
    setEditando(nuevoEditando);
  };

  const seleccionarSugerencia = (index, sugerencia) => {
    actualizarIncidencia(index, sugerencia);
  };

  const guardarCorrecciones = async () => {
    setGuardando(true);
    try {
      const headers = {};
      if (token) headers["Authorization"] = `Token ${token}`;

      const lineasCorregidas = incidencias
        .filter((_, idx) => editando[idx])
        .map((inc, idx) => {
          return `${inc.numLinea}|${editando[idx]}`;
        })
        .join("\n");

      const formData = new FormData();
      formData.append(
        "correcciones",
        new Blob([lineasCorregidas], { type: "text/csv" }),
        "correcciones.csv",
      );
      formData.append("importacion_id", importacionId);

      await axios.post(
        `${API_URL}/api/importaciones/${importacionId}/aplicar_correcciones/`,
        formData,
        { headers },
      );

      setError("");
      alert("Correcciones guardadas exitosamente");
      cargarIncidencias();
    } catch (err) {
      setError("Error guardando correcciones: " + err.message);
    } finally {
      setGuardando(false);
    }
  };

  if (loading) {
    return <div className="info">Cargando incidencias...</div>;
  }

  return (
    <div>
      <h2>Resolución de Incidencias</h2>

      {error && <div className="error">{error}</div>}

      {!incidencias || incidencias.length === 0 ? (
        <div className="info">No hay incidencias que resolver.</div>
      ) : (
        <>
          <p style={{ fontSize: "13px", color: "#666" }}>
            Se encontraron <strong>{incidencias.length}</strong> incidencias que
            requieren corrección manual.
          </p>

          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th style={{ width: "60px" }}>Línea</th>
                  <th style={{ width: "200px" }}>Valor Original</th>
                  <th style={{ width: "150px" }}>Error</th>
                  <th style={{ width: "250px" }}>Sugerencias</th>
                  <th style={{ width: "150px" }}>Corrección</th>
                </tr>
              </thead>
              <tbody>
                {incidencias.map((inc, idx) => (
                  <tr key={idx}>
                    <td>{inc.numLinea}</td>
                    <td style={{ fontSize: "11px", fontFamily: "monospace" }}>
                      {inc.original}
                    </td>
                    <td style={{ fontSize: "11px", color: "#ba2121" }}>
                      {inc.error}
                    </td>
                    <td>
                      {inc.sugerencias && inc.sugerencias.length > 0 ? (
                        <div
                          style={{
                            display: "flex",
                            gap: "5px",
                            flexWrap: "wrap",
                          }}
                        >
                          {inc.sugerencias.map((sug, i) => (
                            <button
                              key={i}
                              onClick={() => seleccionarSugerencia(idx, sug)}
                              className="btn btn-small"
                              style={{
                                background:
                                  editando[idx] === sug ? "#28a745" : "#417690",
                              }}
                            >
                              {sug}
                            </button>
                          ))}
                        </div>
                      ) : (
                        <span style={{ color: "#999" }}>Ninguna</span>
                      )}
                    </td>
                    <td>
                      <input
                        type="text"
                        value={editando[idx] || ""}
                        onChange={(e) =>
                          actualizarIncidencia(idx, e.target.value)
                        }
                        placeholder="Escribir corrección"
                        style={{
                          width: "100%",
                          padding: "6px 8px",
                          border: "1px solid #ddd",
                          borderRadius: "3px",
                          fontSize: "11px",
                        }}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div style={{ marginTop: "20px", textAlign: "right" }}>
            <button
              onClick={guardarCorrecciones}
              disabled={guardando}
              className="btn btn-success"
            >
              {guardando ? "Guardando..." : "Guardar Correcciones"}
            </button>
          </div>
        </>
      )}

      <style>{`
        table td input {
          font-family: "Helvetica", "Arial", sans-serif;
        }
      `}</style>
    </div>
  );
}
