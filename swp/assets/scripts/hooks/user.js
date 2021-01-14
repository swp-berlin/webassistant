const UserData = (() => {
    const node = document.getElementById('user-data');
    const data = JSON.parse(node.textContent);
    node.parentNode.removeChild(node);

    return data;
})();

export const useUser = () => UserData;

export const usePermission = perm => useUser().permissions.includes(perm);
