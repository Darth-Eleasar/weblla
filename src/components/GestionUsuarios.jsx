// Programa: Weblla
// Version: 1.0
// Autor: Equipo Weblla
// Fecha: 02-02-2026
// Descripción: Componente para gestión de usuarios (CRUD)

import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "";

export default function GestionUsuarios({ token, usuario }) {
  const [usuarios, setUsuarios] = useState([]);
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [modalAbierto, setModalAbierto] = useState(false);
  const [usuarioEditando, setUsuarioEditando] = useState(null);
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    first_name: "",
    last_name: "",
    telefono: "",
    rol: "",
    password: "",
    is_active: true,
  });

  // Verificar si el usuario actual es Admin o Ingeniería
  const esAdmin = usuario?.grupos?.some(
    (g) => g === "Admin" || g === "Ingenieria",
  );

  useEffect(() => {
    cargarUsuarios();
    cargarRoles();
  }, []);

  const cargarUsuarios = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/api/usuarios/`, {
        headers: { Authorization: `Token ${token}` },
      });

      // CAMBIO AQUÍ: Comprobamos si viene paginado o es una lista directa
      const data = response.data;
      if (data.results && Array.isArray(data.results)) {
        setUsuarios(data.results);
      } else if (Array.isArray(data)) {
        setUsuarios(data);
      } else {
        setUsuarios([]); // Por seguridad, si no es ninguno, array vacío
      }
    } catch (err) {
      setError("Error al cargar usuarios");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const cargarRoles = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/usuarios/roles/`, {
        headers: { Authorization: `Token ${token}` },
      });
      setRoles(response.data);
    } catch (err) {
      console.error("Error al cargar roles:", err);
    }
  };

  const abrirModal = (user = null) => {
    if (user) {
      setUsuarioEditando(user);
      setFormData({
        username: user.username || "",
        email: user.email || "",
        first_name: user.first_name || "",
        last_name: user.last_name || "",
        telefono: user.telefono || "",
        rol: user.grupos?.[0] || "",
        password: "",
        is_active: user.is_active,
      });
    } else {
      setUsuarioEditando(null);
      setFormData({
        username: "",
        email: "",
        first_name: "",
        last_name: "",
        telefono: "",
        rol: "",
        password: "",
        is_active: true,
      });
    }
    setModalAbierto(true);
  };

  const cerrarModal = () => {
    setModalAbierto(false);
    setUsuarioEditando(null);
    setError("");
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const datos = { ...formData };

      // No enviar password si está vacío (edición)
      if (!datos.password) {
        delete datos.password;
      }

      if (usuarioEditando) {
        // Editar usuario existente
        await axios.patch(
          `${API_URL}/api/usuarios/${usuarioEditando.id}/`,
          datos,
          { headers: { Authorization: `Token ${token}` } },
        );
      } else {
        // Crear nuevo usuario
        if (!datos.password) {
          setError("La contraseña es obligatoria para nuevos usuarios");
          return;
        }
        await axios.post(`${API_URL}/api/usuarios/`, datos, {
          headers: { Authorization: `Token ${token}` },
        });
      }

      cerrarModal();
      cargarUsuarios();
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data?.username?.[0] ||
          err.response?.data?.error ||
          "Error al guardar usuario",
      );
    }
  };

  const handleDesactivar = async (user) => {
    if (!window.confirm(`¿Desactivar al usuario "${user.username}"?`)) {
      return;
    }

    try {
      await axios.delete(`${API_URL}/api/usuarios/${user.id}/`, {
        headers: { Authorization: `Token ${token}` },
      });
      cargarUsuarios();
    } catch (err) {
      setError(err.response?.data?.error || "Error al desactivar usuario");
    }
  };

  const handleActivar = async (user) => {
    try {
      await axios.post(
        `${API_URL}/api/usuarios/${user.id}/activar/`,
        {},
        { headers: { Authorization: `Token ${token}` } },
      );
      cargarUsuarios();
    } catch (err) {
      setError(err.response?.data?.error || "Error al activar usuario");
    }
  };

  if (loading) {
    return <div className="loading">Cargando usuarios...</div>;
  }

  return (
    <div className="gestion-usuarios">
      <div className="header-section">
        <h2>Gestion de Usuarios</h2>
        {esAdmin && (
          <button className="btn btn-primary" onClick={() => abrirModal()}>
            + Nuevo Usuario
          </button>
        )}
      </div>

      {error && <div className="error-message">{error}</div>}

      <table className="tabla-usuarios">
        <thead>
          <tr>
            <th>Usuario</th>
            <th>Nombre</th>
            <th>Email</th>
            <th>Telefono</th>
            <th>Rol</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {usuarios.map((user) => (
            <tr key={user.id} className={!user.is_active ? "inactivo" : ""}>
              <td>{user.username}</td>
              <td>
                {user.first_name} {user.last_name}
              </td>
              <td>{user.email}</td>
              <td>{user.telefono || "-"}</td>
              <td>
                {user.grupos?.length > 0 ? (
                  <span className="badge-rol">{user.grupos.join(", ")}</span>
                ) : (
                  <span className="badge-sin-rol">Sin rol</span>
                )}
              </td>
              <td>
                {user.is_active ? (
                  <span className="badge-activo">Activo</span>
                ) : (
                  <span className="badge-inactivo">Inactivo</span>
                )}
              </td>
              <td>
                <button
                  className="btn btn-small"
                  onClick={() => abrirModal(user)}
                  title="Editar"
                >
                  Editar
                </button>
                {esAdmin && user.id !== usuario.id && (
                  <>
                    {user.is_active ? (
                      <button
                        className="btn btn-small btn-danger"
                        onClick={() => handleDesactivar(user)}
                        title="Desactivar"
                      >
                        Desactivar
                      </button>
                    ) : (
                      <button
                        className="btn btn-small btn-success"
                        onClick={() => handleActivar(user)}
                        title="Activar"
                      >
                        Activar
                      </button>
                    )}
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Modal de edición/creación */}
      {modalAbierto && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>{usuarioEditando ? "Editar Usuario" : "Nuevo Usuario"}</h3>
              <button className="btn-cerrar" onClick={cerrarModal}>
                X
              </button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                <div className="form-group">
                  <label>Usuario *</label>
                  <input
                    type="text"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                    disabled={usuarioEditando && !esAdmin}
                  />
                </div>

                <div className="form-group">
                  <label>Email *</label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Nombre</label>
                  <input
                    type="text"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleChange}
                  />
                </div>

                <div className="form-group">
                  <label>Apellidos</label>
                  <input
                    type="text"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleChange}
                  />
                </div>

                <div className="form-group">
                  <label>Telefono</label>
                  <input
                    type="tel"
                    name="telefono"
                    value={formData.telefono}
                    onChange={handleChange}
                  />
                </div>

                {esAdmin && (
                  <div className="form-group">
                    <label>Rol</label>
                    <select
                      name="rol"
                      value={formData.rol}
                      onChange={handleChange}
                    >
                      <option value="">-- Sin rol --</option>
                      {roles.map((rol) => (
                        <option key={rol.id} value={rol.name}>
                          {rol.name}
                        </option>
                      ))}
                    </select>
                  </div>
                )}

                <div className="form-group">
                  <label>
                    {usuarioEditando
                      ? "Nueva Contrasena (dejar vacio para no cambiar)"
                      : "Contrasena *"}
                  </label>
                  <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    required={!usuarioEditando}
                  />
                </div>
              </div>

              {error && <div className="error-message">{error}</div>}

              <div className="modal-footer">
                <button type="button" className="btn" onClick={cerrarModal}>
                  Cancelar
                </button>
                <button type="submit" className="btn btn-primary">
                  {usuarioEditando ? "Guardar Cambios" : "Crear Usuario"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <style>{`
        .gestion-usuarios {
          padding: 20px;
        }

        .header-section {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
        }

        .header-section h2 {
          margin: 0;
        }

        .error-message {
          background: #f8d7da;
          color: #721c24;
          padding: 10px 15px;
          border-radius: 4px;
          margin-bottom: 15px;
        }

        .tabla-usuarios {
          width: 100%;
          border-collapse: collapse;
          background: white;
          box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .tabla-usuarios th,
        .tabla-usuarios td {
          padding: 12px 15px;
          text-align: left;
          border-bottom: 1px solid #ddd;
        }

        .tabla-usuarios th {
          background: #417690;
          color: white;
          font-weight: 600;
        }

        .tabla-usuarios tr:hover {
          background: #f5f5f5;
        }

        .tabla-usuarios tr.inactivo {
          background: #f8f8f8;
          color: #999;
        }

        .badge-rol {
          background: #417690;
          color: white;
          padding: 3px 8px;
          border-radius: 3px;
          font-size: 12px;
        }

        .badge-sin-rol {
          background: #ddd;
          color: #666;
          padding: 3px 8px;
          border-radius: 3px;
          font-size: 12px;
        }

        .badge-activo {
          background: #28a745;
          color: white;
          padding: 3px 8px;
          border-radius: 3px;
          font-size: 12px;
        }

        .badge-inactivo {
          background: #dc3545;
          color: white;
          padding: 3px 8px;
          border-radius: 3px;
          font-size: 12px;
        }

        .btn {
          padding: 8px 16px;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-size: 14px;
          background: #6c757d;
          color: white;
        }

        .btn:hover {
          opacity: 0.9;
        }

        .btn-primary {
          background: #417690;
        }

        .btn-danger {
          background: #dc3545;
        }

        .btn-success {
          background: #28a745;
        }

        .btn-small {
          padding: 5px 10px;
          font-size: 12px;
          margin-right: 5px;
        }

        /* Modal */
        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0,0,0,0.5);
          display: flex;
          justify-content: center;
          align-items: center;
          z-index: 1000;
        }

        .modal {
          background: white;
          border-radius: 8px;
          width: 90%;
          max-width: 600px;
          max-height: 90vh;
          overflow-y: auto;
        }

        .modal-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 15px 20px;
          border-bottom: 1px solid #ddd;
          background: #417690;
          color: white;
          border-radius: 8px 8px 0 0;
        }

        .modal-header h3 {
          margin: 0;
        }

        .btn-cerrar {
          background: transparent;
          border: none;
          color: white;
          font-size: 18px;
          cursor: pointer;
          padding: 5px 10px;
        }

        .modal form {
          padding: 20px;
        }

        .form-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 15px;
        }

        .form-group {
          display: flex;
          flex-direction: column;
        }

        .form-group label {
          margin-bottom: 5px;
          font-weight: 600;
          font-size: 13px;
          color: #333;
        }

        .form-group input,
        .form-group select {
          padding: 8px 10px;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 14px;
        }

        .form-group input:focus,
        .form-group select:focus {
          outline: none;
          border-color: #417690;
        }

        .form-group input:disabled {
          background: #f5f5f5;
          cursor: not-allowed;
        }

        .modal-footer {
          display: flex;
          justify-content: flex-end;
          gap: 10px;
          padding-top: 15px;
          border-top: 1px solid #ddd;
          margin-top: 15px;
        }

        .loading {
          text-align: center;
          padding: 40px;
          color: #666;
        }

        @media (max-width: 600px) {
          .form-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
}
