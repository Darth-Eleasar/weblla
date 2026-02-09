// Programa: Weblla
// Veersion: 1.1
// Autor: Equipo Weblla
// Fecha: 28-01-2026
// Última Modificación: 02-02-2026
// Cambios realizados:
// - 02-02-2026: Añadida gestión de sesión y menú dinámico basado en permisos de usuario.
// - 28-01-2026: Creación del componente principal App.jsx.
// Descripción:
// Componente principal de la aplicación React para el control de huellas.

import React, { useState, useEffect } from "react";
import HuellaList from "./components/HuellaList";
import Importaciones from "./components/Importaciones";
import ResolucionIncidencias from "./components/ResolucionIncidencias";
import Login from "./components/Login";
import GestionUsuarios from "./components/GestionUsuarios";

export default function App() {
  const [vista, setVista] = useState("lista");
  const [usuario, setUsuario] = useState(null);
  const [token, setToken] = useState(null);
  const [menu, setMenu] = useState(null);
  const [cargando, setCargando] = useState(true);

  // Verificar si hay sesión guardada al cargar la app
  useEffect(() => {
    const token_guardado = localStorage.getItem("token");
    const user_guardado = localStorage.getItem("user");
    const menu_guardado = localStorage.getItem("menu");

    if (token_guardado && user_guardado) {
      setToken(token_guardado);
      setUsuario(JSON.parse(user_guardado));
      if (menu_guardado) {
        setMenu(JSON.parse(menu_guardado));
      }
    }
    setCargando(false);
  }, []);

  const handleLoginSuccess = (user, token, menu) => {
    setUsuario(user);
    setToken(token);
    setMenu(menu);
    localStorage.setItem("menu", JSON.stringify(menu));
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    localStorage.removeItem("menu");
    setUsuario(null);
    setToken(null);
    setMenu(null);
  };

  // Si no hay sesión, mostrar login
  if (!usuario || !token || cargando) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="app">
      <header>
        <h1>Weblla • Control de Huella</h1>
        <div className="user-info">
          <span>
            👤 {usuario.username}{" "}
            {usuario.grupos.length > 0 && `• ${usuario.grupos.join(", ")}`}
          </span>
          <a
            href="#"
            onClick={(e) => {
              e.preventDefault();
              handleLogout();
            }}
          >
            Salir
          </a>
        </div>
      </header>

      <div style={{ display: "flex", flex: 1 }}>
        <div className="nav-container">
          <ul className="nav-links">
            {menu?.mostrar_huellas && (
              <li>
                <a
                  href="#"
                  className={vista === "lista" ? "active" : ""}
                  onClick={(e) => {
                    e.preventDefault();
                    setVista("lista");
                  }}
                >
                  📋 Huellas
                </a>
              </li>
            )}
            {menu?.mostrar_importar && (
              <li>
                <a
                  href="#"
                  className={vista === "importar" ? "active" : ""}
                  onClick={(e) => {
                    e.preventDefault();
                    setVista("importar");
                  }}
                >
                  📤 Importar CSV
                </a>
              </li>
            )}
            {menu?.mostrar_reportes && (
              <li>
                <a
                  href="#"
                  className={vista === "reportes" ? "active" : ""}
                  onClick={(e) => {
                    e.preventDefault();
                    setVista("reportes");
                  }}
                >
                  📊 Reportes
                </a>
              </li>
            )}
            {menu?.mostrar_usuarios && (
              <li>
                <a
                  href="#"
                  className={vista === "usuarios" ? "active" : ""}
                  onClick={(e) => {
                    e.preventDefault();
                    setVista("usuarios");
                  }}
                >
                  👥 Usuarios
                </a>
              </li>
            )}
            {menu?.mostrar_resolucion && (
              <li>
                <a
                  href="#"
                  className={vista === "resolucion" ? "active" : ""}
                  onClick={(e) => {
                    e.preventDefault();
                    setVista("resolucion");
                  }}
                >
                  🔧 Incidencias
                </a>
              </li>
            )}
          </ul>
        </div>

        <div className="content">
          {vista === "lista" && <HuellaList token={token} usuario={usuario} />}
          {vista === "importar" && (
            <Importaciones token={token} usuario={usuario} />
          )}
          {vista === "reportes" && (
            <div>
              <h2>Reportes</h2>
              <p>Función de reportes en desarrollo...</p>
            </div>
          )}
          {vista === "usuarios" && (
            <GestionUsuarios token={token} usuario={usuario} />
          )}
          {vista === "resolucion" && (
            <ResolucionIncidencias token={token} usuario={usuario} />
          )}
        </div>
      </div>
    </div>
  );
}
