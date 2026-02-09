// Programa: Weblla
// Veersion: 1.0
// Autor: Equipo Weblla
// Fecha: 28-01-2026
// Descripción: Componente de Login para la aplicación Weblla.
// Maneja la autenticación del usuario y la configuración del menú.
// Utiliza React y Axios para las solicitudes HTTP.
// Almacena el token de autenticación y la configuración del usuario en localStorage.
// Permite la personalización del menú basado en la respuesta del servidor.
// Proporciona retroalimentación al usuario durante el proceso de inicio de sesión.

import React, { useState } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "";

export default function Login({ onLoginSuccess }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await axios.post(`${API_URL}/api/auth/login/`, {
        username,
        password,
      });

      const { token, user } = response.data;

      // Obtener configuración de menú
      let menu = user.menu || {
        mostrar_huellas: true,
        mostrar_importar: false,
        mostrar_reportes: false,
        mostrar_usuarios: false,
        mostrar_resolucion: false,
      };

      // Guardar token en localStorage
      localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(user));
      localStorage.setItem("menu", JSON.stringify(menu));

      // Llamar callback de login exitoso
      if (onLoginSuccess) {
        onLoginSuccess(user, token, menu);
      }
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data?.non_field_errors?.[0] ||
          "Error en la autenticación",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-wrapper">
      <div className="login-container">
        <div className="login-box">
          <div className="login-header">
            <h1>Weblla</h1>
            <h2>Control de Huella Óptica</h2>
          </div>

          {error && <div className="error">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="username">Usuario</label>
              <input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Contraseña</label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loading}
              />
            </div>

            <button
              type="submit"
              className="btn"
              disabled={loading}
              style={{ width: "100%" }}
            >
              {loading ? "Autenticando..." : "Iniciar Sesión"}
            </button>
          </form>

          <div className="login-footer">
            <p>
              <strong>Demo:</strong>
              <br />
              Usuario: <code>admin</code>
              <br />
              Contraseña: <code>admin</code>
            </p>
          </div>
        </div>
      </div>

      <style>{`
        .login-wrapper {
          display: flex;
          justify-content: center;
          align-items: center;
          min-height: 100vh;
          background: #f8f9fa;
        }

        .login-container {
          width: 100%;
          max-width: 350px;
        }

        .login-box {
          background: white;
          border: 1px solid #ddd;
          border-radius: 4px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .login-header {
          background: #417690;
          color: white;
          padding: 30px 20px;
          text-align: center;
          border-radius: 4px 4px 0 0;
        }

        .login-header h1 {
          margin: 0 0 5px 0;
          font-size: 28px;
          font-weight: 600;
        }

        .login-header h2 {
          margin: 0;
          font-size: 13px;
          font-weight: 400;
          opacity: 0.95;
        }

        form {
          padding: 20px;
        }

        .form-group {
          margin-bottom: 15px;
        }

        label {
          display: block;
          margin-bottom: 5px;
          font-weight: 600;
          font-size: 12px;
          color: #333;
        }

        input[type="text"],
        input[type="password"] {
          width: 100%;
          padding: 8px 10px;
          border: 1px solid #ddd;
          background: white;
          color: #333;
          font-size: 12px;
          box-sizing: border-box;
          font-family: "Helvetica", "Arial", sans-serif;
        }

        input:focus {
          outline: none;
          border-color: #417690;
          box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.08);
        }

        input:disabled {
          background: #f5f5f5;
          cursor: not-allowed;
        }

        .login-footer {
          padding: 15px 20px;
          border-top: 1px solid #eee;
          background: #f8f9fa;
          border-radius: 0 0 4px 4px;
          font-size: 11px;
          color: #666;
        }

        .login-footer p {
          margin: 0;
          line-height: 1.6;
        }

        .login-footer code {
          background: #f0f0f0;
          padding: 2px 4px;
          border-radius: 2px;
          font-family: monospace;
          color: #333;
        }
      `}</style>
    </div>
  );
}
