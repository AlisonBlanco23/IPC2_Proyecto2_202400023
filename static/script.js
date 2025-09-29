document.addEventListener('DOMContentLoaded', function() {
    const invernaderoSelect = document.getElementById('invernadero');
    const planSelect = document.getElementById('plan');

    if (!invernaderoSelect || !planSelect) return;

    invernaderoSelect.addEventListener('change', function() {
        const invNombre = this.value.trim();
        planSelect.innerHTML = '<option value="">Cargando planes...</option>';
        planSelect.disabled = true;

        if (!invNombre) {
            planSelect.innerHTML = '<option value="">Seleccionar invernadero primero</option>';
            return;
        }

        fetch(`/get-plans?invernadero=${encodeURIComponent(invNombre)}`)
            .then(response => response.json())
            .then(data => {
                planSelect.innerHTML = '';
                if (data.planes?.length > 0) {
                    data.planes.forEach(plan => {
                        const opt = document.createElement('option');
                        opt.value = plan;
                        opt.textContent = plan;
                        planSelect.appendChild(opt);
                    });
                } else {
                    planSelect.innerHTML = '<option value="">No hay planes</option>';
                }
                planSelect.disabled = false;
            })
            .catch(() => {
                planSelect.innerHTML = '<option value="">Error al cargar</option>';
                planSelect.disabled = false;
            });
    });
});
