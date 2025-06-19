document.addEventListener('DOMContentLoaded', function() {
    const cadastroForm = document.getElementById('cadastroForm');
    const mensagemDiv = document.getElementById('mensagem');
    const userTableBody = document.querySelector('#userTable tbody');
    const noUsersMessage = document.getElementById('noUsersMessage');
    const submitButton = cadastroForm.querySelector('button[type="submit"]');
    const senhaInput = document.getElementById('senha');
    const senhaHelp = document.getElementById('senhaHelp');

    let editingUserId = null;

    async function fetchUsers() {
        try {
            const response = await fetch('/usuarios');
            if (!response.ok) {
                throw new Error('Falha ao buscar usuários.');
            }
            const users = await response.json();

            userTableBody.innerHTML = '';
            if (users.length === 0) {
                noUsersMessage.style.display = 'block';
            } else {
                noUsersMessage.style.display = 'none';
                users.forEach(user => {
                    const row = userTableBody.insertRow();
                    row.insertCell().textContent = user.id;
                    row.insertCell().textContent = user.nome;
                    row.insertCell().textContent = user.email;
                    const actionsCell = row.insertCell();
                    actionsCell.innerHTML = `
                        <button class="btn-action btn-edit" data-id="${user.id}" data-nome="${user.nome}" data-email="${user.email}">Editar</button>
                        <button class="btn-action btn-delete" data-id="${user.id}">Excluir</button>
                    `;
                });
            }
        } catch (error) {
            console.error('Erro ao carregar usuários:', error);
            noUsersMessage.textContent = 'Erro ao carregar usuários.';
            noUsersMessage.style.display = 'block';
        }
    }

    userTableBody.addEventListener('click', async function(event) {
        if (event.target.classList.contains('btn-edit')) {
            const button = event.target;
            const id = button.dataset.id;
            const nome = button.dataset.nome;
            const email = button.dataset.email;

            document.getElementById('nome').value = nome;
            document.getElementById('email').value = email;
            senhaInput.value = '';
            senhaInput.placeholder = 'Deixe em branco para manter a senha atual ou digite uma nova';
            senhaInput.required = false;
            senhaHelp.style.display = 'block';

            editingUserId = id;
            submitButton.textContent = 'Salvar Alterações';
            submitButton.style.backgroundColor = 'var(--warning-yellow)';
            submitButton.style.color = 'var(--dark-text)';

            mensagemDiv.textContent = 'Editando usuário. Digite uma nova senha se desejar alterá-la.';
            mensagemDiv.classList.remove('success', 'error');
            mensagemDiv.classList.add('info');

            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else if (event.target.classList.contains('btn-delete')) {
            const userIdToDelete = event.target.dataset.id;
            if (confirm(`Tem certeza que deseja excluir o usuário com ID ${userIdToDelete}?`)) {
                try {
                    const response = await fetch(`/usuarios/${userIdToDelete}`, {
                        method: 'DELETE'
                    });

                    const data = await response.json();

                    if (response.ok) {
                        mensagemDiv.textContent = data.message || 'Usuário excluído com sucesso!';
                        mensagemDiv.classList.add('success');
                        fetchUsers();
                    } else {
                        mensagemDiv.textContent = data.error || 'Erro ao excluir usuário.';
                        mensagemDiv.classList.add('error');
                    }
                } catch (error) {
                    console.error('Erro na requisição de exclusão:', error);
                    mensagemDiv.textContent = 'Ocorreu um erro na conexão ao excluir usuário.';
                    mensagemDiv.classList.add('error');
                }
            }
        }
    });

    cadastroForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const nome = document.getElementById('nome').value;
        const email = document.getElementById('email').value;
        const senha = document.getElementById('senha').value;

        mensagemDiv.textContent = '';
        mensagemDiv.className = 'message';

        if (!nome || !email) {
            mensagemDiv.textContent = 'Nome e Email são obrigatórios.';
            mensagemDiv.classList.add('error');
            return;
        }

        if (!editingUserId && !senha) {
            mensagemDiv.textContent = 'A senha é obrigatória para novos cadastros.';
            mensagemDiv.classList.add('error');
            return;
        }

        let url = '/cadastrar';
        let method = 'POST';
        let payload = { nome, email };
        if (senha) {
            payload.senha = senha;
        } else if (!editingUserId) {
             mensagemDiv.textContent = 'A senha é obrigatória para novos cadastros.';
             mensagemDiv.classList.add('error');
             return;
        }


        if (editingUserId) {
            url = `/usuarios/${editingUserId}`;
            method = 'PUT';
        }

        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok) {
                mensagemDiv.textContent = data.message || (editingUserId ? 'Usuário atualizado com sucesso!' : 'Usuário cadastrado com sucesso!');
                mensagemDiv.classList.add('success');
                cadastroForm.reset();

                editingUserId = null;
                submitButton.textContent = 'Cadastrar';
                submitButton.style.backgroundColor = '';
                submitButton.style.color = '';
                senhaInput.required = true;
                senhaHelp.style.display = 'none';

                fetchUsers();
            } else {
                mensagemDiv.textContent = data.error || (editingUserId ? 'Erro desconhecido ao atualizar usuário.' : 'Erro desconhecido ao cadastrar usuário.');
                mensagemDiv.classList.add('error');
            }

        } catch (error) {
            console.error('Erro na requisição:', error);
            mensagemDiv.textContent = 'Ocorreu um erro na conexão com o servidor. Tente novamente.';
            mensagemDiv.classList.add('error');
        }
    });

    fetchUsers();
});