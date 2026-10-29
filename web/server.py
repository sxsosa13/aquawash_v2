<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sosa Car Wash</title>
  <style>
    :root {
      --azul: #0a66c2;
      --celeste: #7ecbff;
      --azul-oscuro: #083b6b;
      --blanco: #ffffff;
      --gris: #edf6ff;
      --gris-oscuro: #4d6275;
      --texto: #12314a;
      --borde: #dfeeff;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background: var(--gris);
      color: var(--texto);
    }
    a { text-decoration: none; }
    .container { width: min(1100px, 90%); margin: 0 auto; }
    header {
      background: linear-gradient(135deg, var(--azul), var(--celeste));
      color: var(--blanco);
      padding-bottom: 60px;
    }
    nav {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px 0;
      flex-wrap: wrap;
      gap: 20px;
    }
    .brand {
      font-size: 2rem;
      font-weight: 700;
      letter-spacing: 0.03em;
    }
    .nav-links {
      display: flex;
      gap: 20px;
      flex-wrap: wrap;
    }
    .nav-links a {
      color: var(--blanco);
      font-weight: 600;
    }
    .hero {
      display: grid;
      grid-template-columns: 1.2fr 0.8fr;
      gap: 30px;
      align-items: center;
      padding-top: 25px;
    }
    .hero h1 {
      font-size: clamp(2.2rem, 4vw, 4rem);
      margin: 0 0 18px;
      line-height: 1.1;
    }
    .hero p {
      font-size: 1.08rem;
      line-height: 1.7;
      margin: 0 0 22px;
      max-width: 620px;
    }
    .cta {
      display: inline-block;
      background: var(--blanco);
      color: var(--azul);
      padding: 16px 28px;
      border-radius: 12px;
      font-weight: 700;
      box-shadow: 0 16px 28px rgba(0,0,0,0.12);
    }
    .card {
      background: var(--blanco);
      border-radius: 18px;
      box-shadow: 0 14px 30px rgba(8, 59, 107, 0.12);
      padding: 24px;
      color: var(--texto);
    }
    .tag {
      display: inline-block;
      background: rgba(255,255,255,0.15);
      border: 1px solid rgba(255,255,255,0.3);
      border-radius: 999px;
      padding: 8px 14px;
      margin-bottom: 16px;
      font-weight: 600;
    }
    .section {
      padding: 80px 0;
    }
    .section h2 {
      text-align: center;
      font-size: clamp(2rem, 3vw, 2.5rem);
      margin: 0 0 26px;
    }
    .cards {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 22px;
      margin-top: 30px;
    }
    .servicio {
      background: var(--blanco);
      border-radius: 18px;
      padding: 24px;
      box-shadow: 0 10px 22px rgba(0, 0, 0, 0.05);
      border: 1px solid var(--borde);
    }
    .servicio h3 {
      margin-top: 0;
      color: var(--azul-oscuro);
    }
    .precio {
      font-size: 1.7rem;
      font-weight: 700;
      color: var(--azul);
      margin-top: 14px;
    }
    .grid-form {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 26px;
      margin-top: 20px;
    }
    input, select, textarea, button {
      width: 100%;
      padding: 12px 14px;
      border-radius: 10px;
      border: 1px solid var(--borde);
      font-size: 1rem;
      margin-top: 10px;
      font-family: inherit;
    }
    textarea {
      min-height: 120px;
      resize: vertical;
    }
    button {
      background: linear-gradient(135deg, var(--azul), var(--celeste));
      border: none;
      color: var(--blanco);
      font-weight: 700;
      cursor: pointer;
    }
    .info-list {
      line-height: 1.8;
      color: var(--gris-oscuro);
    }
    .status-box {
      margin-top: 14px;
      padding: 12px;
      border-radius: 10px;
      background: #ecfff0;
      color: #0d6b3a;
      display: none;
    }
    .status-box.visible { display: block; }
    .status-box.error {
      background: #fff0f0;
      color: #a12626;
    }
    @media (max-width: 760px) {
      .hero, .cards, .grid-form { grid-template-columns: 1fr; }
      nav { justify-content: center; }
    }
  </style>
</head>
<body>
  <header>
    <div class="container">
      <nav>
        <div class="brand">Sosa Car Wash</div>
        <div class="nav-links">
          <a href="#servicios">Servicios</a>
          <a href="#reservar">Reservar</a>
          <a href="#seguimiento">Seguimiento</a>
          <a href="#contacto">Contacto</a>
        </div>
      </nav>
      <div class="hero">
        <div>
          <div class="tag">Lavado premium para autos y motos</div>
          <h1>Tu vehículo merece brillo, cuidado y confianza.</h1>
          <p>En Sosa Car Wash cuidamos cada detalle con atención de calidad, rapidez y servicio profesional para mantener tu vehículo impecable.</p>
          <a href="#reservar" class="cta">Reservar ahora</a>
        </div>
        <div class="card">
          <h3>Agenda disponible</h3>
          <p>Horario: 08:00 a 17:00</p>
          <p>Servicios: lavado básico, completo y premium</p>
          <p>Pago: guaraní (₲)</p>
        </div>
      </div>
    </div>
  </header>

  <main>
    <section class="section" id="servicios">
      <div class="container">
        <h2>Servicios destacados</h2>
        <div class="cards">
          <div class="servicio">
            <h3>Lavado básico</h3>
            <p>Ideal para limpieza general y mantenimiento diario.</p>
            <div class="precio">₲ 100.000</div>
          </div>
          <div class="servicio">
            <h3>Lavado completo</h3>
            <p>Enjuague profundo, secado, terminado y detalle final.</p>
            <div class="precio">₲ 180.000</div>
          </div>
          <div class="servicio">
            <h3>Premium</h3>
            <p>Servicio completo con abrillantado y cuidado especial.</p>
            <div class="precio">₲ 260.000</div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="reservar">
      <div class="container">
        <h2>Reservar turno</h2>
        <div class="grid-form">
          <div class="card">
            <h3>Solicita tu cita</h3>
            <form id="reservaForm">
              <input type="text" name="nombre" placeholder="Nombre completo" required>
              <input type="tel" name="telefono" placeholder="Teléfono" required>
              <select name="tipo" required>
                <option value="AUTO">Auto</option>
                <option value="MOTO">Moto</option>
              </select>
              <select name="servicio" required>
                <option value="Lavado básico">Lavado básico</option>
                <option value="Lavado completo">Lavado completo</option>
                <option value="Premium">Premium</option>
              </select>
              <input type="date" name="fecha" required>
              <input type="time" name="hora" required>
              <button type="submit">Reservar</button>
            </form>
            <div id="statusReserva" class="status-box"></div>
          </div>
          <div class="card">
            <h3>¿Por qué elegirnos?</h3>
            <div class="info-list">
              <div>✔ Atención rápida y ordenada</div>
              <div>✔ Servicios para autos y motos</div>
              <div>✔ Precios claros en guaraní</div>
              <div>✔ Control profesional y seguimiento</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="seguimiento">
      <div class="container">
        <h2>Seguimiento de reserva</h2>
        <div class="card" style="max-width: 600px; margin: 0 auto;">
          <h3>Consultar estado</h3>
          <form id="trackForm">
            <input type="text" name="codigo" placeholder="Código de reserva" required>
            <button type="submit">Consultar</button>
          </form>
          <div id="statusTrack" class="status-box"></div>
        </div>
      </div>
    </section>

    <section class="section" id="contacto">
      <div class="container">
        <h2>Contacto</h2>
        <div class="grid-form">
          <div class="card">
            <h3>Datos del negocio</h3>
            <div class="info-list">
              <div>📍 Asunción, Paraguay</div>
              <div>📞 +595 981 000000</div>
              <div>✉️ contacto@sosacarwash.com</div>
              <div>🕒 Lunes a sábado: 08:00 a 17:00</div>
            </div>
          </div>
          <div class="card">
            <h3>Envíanos un mensaje</h3>
            <form id="contactForm">
              <input type="text" name="nombre" placeholder="Nombre" required>
              <input type="email" name="email" placeholder="Email" required>
              <input type="tel" name="telefono" placeholder="Teléfono">
              <textarea name="mensaje" placeholder="Mensaje" required></textarea>
              <button type="submit">Enviar</button>
            </form>
            <div id="statusContact" class="status-box"></div>
          </div>
        </div>
      </div>
    </section>
  </main>

  <script>
    const setStatus = (el, msg, kind = 'ok') => {
      el.textContent = msg;
      el.className = 'status-box visible' + (kind === 'error' ? ' error' : '');
    };

    document.getElementById('reservaForm').addEventListener('submit', (e) => {
      e.preventDefault();
      const form = e.target;
      setStatus(document.getElementById('statusReserva'), 'Reserva registrada correctamente. Estaremos en contacto con usted.', 'ok');
      form.reset();
    });

    document.getElementById('trackForm').addEventListener('submit', (e) => {
      e.preventDefault();
      setStatus(document.getElementById('statusTrack'), 'Su reserva está en proceso de atención y será confirmada pronto.', 'ok');
    });

    document.getElementById('contactForm').addEventListener('submit', (e) => {
      e.preventDefault();
      setStatus(document.getElementById('statusContact'), 'Mensaje enviado correctamente. Gracias por contactarnos.', 'ok');
      e.target.reset();
    });
  </script>
</body>
</html>
